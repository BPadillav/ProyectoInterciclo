def create_sharpen_mask(mask_size):
    import numpy as np
    center_value = mask_size * 2 - 1  # Valor central (el más alto)
    surrounding_value = -1           # Valores alrededor (negativos)
    mask_sum = 0

    mask = np.zeros((mask_size, mask_size), dtype=np.int32)

    for i in range(mask_size):
        for j in range(mask_size):
            if i == mask_size // 2 and j == mask_size // 2:
                mask[i, j] = center_value  # Valor central
                mask_sum += center_value
            else:
                mask[i, j] = surrounding_value  # Valores periféricos
                mask_sum += surrounding_value

    return mask.flatten(), mask_sum if mask_sum != 0 else 1


def create_dilation_mask(mask_size):
    import numpy as np
    return np.ones((mask_size, mask_size), dtype=np.int32).flatten()


def process_image(num_threads, filter_type, mask_size, image):
    """
    Procesa la imagen usando el filtro especificado con PyCUDA.
    """
    import numpy as np
    import pycuda.driver as cuda
    from pycuda.compiler import SourceModule
    import time

    # Inicializar el driver de CUDA
    cuda.init()
    device = cuda.Device(0)  # Seleccionar el dispositivo 0
    context = device.make_context()

    try:
        height, width, channels = image.shape
        total_pixels = width * height
        num_blocks = (total_pixels + num_threads - 1) // num_threads

        # Convertir la imagen a un array unidimensional
        h_image = image.astype(np.uint8).flatten()

        # Inicializar el array de salida
        h_output_image = np.zeros_like(h_image)

        # Asignar memoria en GPU
        d_image = cuda.mem_alloc(h_image.nbytes)
        cuda.memcpy_htod(d_image, h_image)
        d_output_image = cuda.mem_alloc(h_image.nbytes)

        time_results = {}

        # Procesamiento según el tipo de filtro
        if filter_type == "sharpen":
            mask_sharpen, mask_sum = create_sharpen_mask(mask_size)
            mask_gpu = cuda.mem_alloc(mask_sharpen.nbytes)
            cuda.memcpy_htod(mask_gpu, mask_sharpen)

            module = SourceModule("""
            __global__ void apply_sharpen_filter(unsigned char* d_in, unsigned char* d_out, int width, int height, int channels, int* mask, int mask_size, int mask_sum) {
                int tid = threadIdx.x + blockIdx.x * blockDim.x;
                int total_pixeles = width * height;

                if (tid < total_pixeles) {
                    int x = tid % width;
                    int y = tid / width;

                    int half_mask = mask_size / 2;
                    int output_pixel[3] = { 0, 0, 0 };

                    // Aplicar la máscara de convolución dinámicamente según su tamaño
                    for (int i = -half_mask; i <= half_mask; i++) {
                        for (int j = -half_mask; j <= half_mask; j++) {
                            int neighbor_x = min(max(x + j, 0), width - 1);
                            int neighbor_y = min(max(y + i, 0), height - 1);
                            int neighbor_index = (neighbor_y * width + neighbor_x) * channels;

                            int mask_value = mask[(i + half_mask) * mask_size + (j + half_mask)];
                            output_pixel[0] += d_in[neighbor_index] * mask_value;      // Red
                            output_pixel[1] += d_in[neighbor_index + 1] * mask_value;  // Green
                            output_pixel[2] += d_in[neighbor_index + 2] * mask_value;  // Blue
                        }
                    }

                    // Normalizar y clampear los valores
                    output_pixel[0] = min(max(output_pixel[0] / mask_sum, 0), 255);
                    output_pixel[1] = min(max(output_pixel[1] / mask_sum, 0), 255);
                    output_pixel[2] = min(max(output_pixel[2] / mask_sum, 0), 255);

                    // Escribir los valores calculados
                    int index = tid * channels;
                    d_out[index] = output_pixel[0];  // Red
                    d_out[index + 1] = output_pixel[1];  // Green
                    d_out[index + 2] = output_pixel[2];  // Blue
                }
            }
            """)
            kernel = module.get_function("apply_sharpen_filter")

            start = time.time()
            kernel(
                d_image, d_output_image,
                np.int32(width), np.int32(height), np.int32(channels),
                mask_gpu, np.int32(mask_size), np.int32(mask_sum),
                block=(num_threads, 1, 1), grid=(num_blocks, 1)
            )
            context.synchronize()
            time_results["gpu_time"] = (time.time() - start) * 1000

        elif filter_type == "dilation":
            mask_dilation = create_dilation_mask(mask_size)
            mask_gpu = cuda.mem_alloc(mask_dilation.nbytes)
            cuda.memcpy_htod(mask_gpu, mask_dilation)

            module = SourceModule("""
            __global__ void apply_dilation_filter(unsigned char* d_in, unsigned char* d_out, int width, int height, int channels, int* mask, int mask_size) {
                int tid = threadIdx.x + blockIdx.x * blockDim.x;
                int total_pixeles = width * height;

                if (tid < total_pixeles) {
                    int x = tid % width;
                    int y = tid / width;

                    int half_mask = mask_size / 2;
                    int max_pixel[3] = { 0, 0, 0 };  // Inicializar al mínimo valor

                    // Aplicar la máscara de dilatación
                    for (int i = -half_mask; i <= half_mask; i++) {
                        for (int j = -half_mask; j <= half_mask; j++) {
                            int neighbor_x = min(max(x + j, 0), width - 1);
                            int neighbor_y = min(max(y + i, 0), height - 1);
                            int neighbor_index = (neighbor_y * width + neighbor_x) * channels;

                            // Obtener el valor máximo en la vecindad
                            max_pixel[0] = max(max_pixel[0], d_in[neighbor_index]);      // Red
                            max_pixel[1] = max(max_pixel[1], d_in[neighbor_index + 1]);  // Green
                            max_pixel[2] = max(max_pixel[2], d_in[neighbor_index + 2]);  // Blue
                        }
                    }

                    // Escribir los valores calculados
                    int index = tid * channels;
                    d_out[index] = max_pixel[0];  // Red
                    d_out[index + 1] = max_pixel[1];  // Green
                    d_out[index + 2] = max_pixel[2];  // Blue
                }
            }
            """)
            kernel = module.get_function("apply_dilation_filter")

            start = time.time()
            kernel(
                d_image, d_output_image,
                np.int32(width), np.int32(height), np.int32(channels),
                mask_gpu, np.int32(mask_size),
                block=(num_threads, 1, 1), grid=(num_blocks, 1)
            )
            context.synchronize()
            time_results["gpu_time"] = (time.time() - start) * 1000

        elif filter_type == "canny":
            module = SourceModule("""
            __global__ void apply_canny_filter(unsigned char* d_in, unsigned char* d_out, int width, int height, int channels, int mask_size) {
                int tid = threadIdx.x + blockIdx.x * blockDim.x;
                int total_pixeles = width * height;

                if (tid < total_pixeles) {
                    int x = tid % width;
                    int y = tid / width;

                    // Definir las máscaras de Sobel para diferentes tamaños de máscara
                    int half_mask = mask_size / 2;
                    float gradient_x = 0.0f;
                    float gradient_y = 0.0f;

                    // Aplicar la máscara Sobel (Canny) con tamaño variable
                    for (int i = -half_mask; i <= half_mask; i++) {
                        for (int j = -half_mask; j <= half_mask; j++) {
                            int neighbor_x = min(max(x + j, 0), width - 1);
                            int neighbor_y = min(max(y + i, 0), height - 1);
                            int neighbor_index = (neighbor_y * width + neighbor_x) * channels;

                            // Operadores de Sobel para 3x3 (pueden ajustarse para otras máscaras)
                            int Gx = j * (mask_size - abs(i));  // Ajuste del gradiente en X
                            int Gy = i * (mask_size - abs(j));  // Ajuste del gradiente en Y

                            gradient_x += d_in[neighbor_index] * Gx;
                            gradient_y += d_in[neighbor_index] * Gy;
                        }
                    }

                    // Magnitud del gradiente
                    float magnitude = sqrtf(gradient_x * gradient_x + gradient_y * gradient_y);

                    int index = tid * channels;

                    // Escribir el resultado (convertir la magnitud a escala de grises)
                    unsigned char pixel_value = min(max(int(magnitude), 0), 255);
                    d_out[index] = pixel_value;  // Red
                    d_out[index + 1] = pixel_value;  // Green
                    d_out[index + 2] = pixel_value;  // Blue
                }
            }
            """)
            kernel = module.get_function("apply_canny_filter")

            start = time.time()
            kernel(
                d_image, d_output_image,
                np.int32(width), np.int32(height), np.int32(channels),
                np.int32(mask_size),
                block=(num_threads, 1, 1), grid=(num_blocks, 1)
            )
            context.synchronize()
            time_results["gpu_time"] = (time.time() - start) * 1000

        else:
            raise ValueError(f"Filtro no reconocido: {filter_type}")

        cuda.memcpy_dtoh(h_output_image, d_output_image)
        processed_image = h_output_image.reshape((height, width, channels))
        return processed_image, time_results

    finally:
        context.pop()
        context.detach()


def allowed_file(filename):
    """
    Validar extensiones de archivo permitidas.
    """
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
