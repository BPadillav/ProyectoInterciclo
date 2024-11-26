import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastController, LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-photo-preview',
  templateUrl: './photo-preview.page.html',
  styleUrls: ['./photo-preview.page.scss'],
})
export class PhotoPreviewPage implements OnInit {
  photo: string | undefined; // Foto original en Base64
  filteredPhoto: string | undefined; // URL de la foto con filtro aplicado
  displayPhoto: string | undefined; // Foto actualmente mostrada (original o filtrada)
  showOriginal: boolean = true; // Estado para alternar entre original y filtro
  private baseUrl: string = '';

  // Filtros estáticos disponibles
  filters = [
    { name: 'Sharpen', value: 'sharpen' },
    { name: 'Dilation', value: 'dilation' },
    { name: 'Canny', value: 'canny' },
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private toastController: ToastController,
    private loadingController: LoadingController
  ) { }

  ngOnInit() {
    this.baseUrl = localStorage.getItem('serverUrl') || 'http://localhost:5000';

    this.route.queryParams.subscribe((params) => {
      this.photo = params['photo'];
      this.displayPhoto = this.photo; // Mostrar la foto original inicialmente
      console.log('Foto cargada (Base64):', this.photo);
    });
  }

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      position: 'bottom',
      color,
    });
    await toast.present();
  }

  toggleOriginal() {
    this.showOriginal = !this.showOriginal;
    this.displayPhoto = this.showOriginal ? this.photo : this.filteredPhoto;
  }

  async savePhoto() {
    if (!this.filteredPhoto && !this.photo) {
      this.showToast('No hay foto para guardar.', 'danger');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('userIDPublic', '1');
      formData.append('contenido', 'Descripción de la foto');
      formData.append('filtroIDPublic', '1');

      let photoBlob: Blob;

      if (this.filteredPhoto?.startsWith('http')) {
        // Descargar la imagen procesada desde la URL del backend
        console.log('Descargando imagen procesada desde URL:', this.filteredPhoto);
        const response = await this.http.get(this.filteredPhoto, { responseType: 'blob' }).toPromise();
        if (!response) {
          throw new Error('No se pudo descargar la imagen procesada.');
        }
        photoBlob = response;
      } else if (this.photo) {
        console.log('Convirtiendo Base64 de la foto original a Blob.');
        photoBlob = this.base64ToBlob(this.photo);
      } else {
        throw new Error('No se pudo procesar la imagen.');
      }

      formData.append('rutaImagen', photoBlob, 'photo.png');
      console.log('FormData creado correctamente:', formData);

      const loading = await this.loadingController.create({
        message: 'Guardando foto...',
      });
      await loading.present();

      this.http.post(`${this.baseUrl}/create_publicacion`, formData).subscribe({
        next: async () => {
          await this.showToast('Publicación creada exitosamente.', 'success');
          this.router.navigate(['/tabs/home']);
          loading.dismiss();
        },
        error: async (error) => {
          console.error('Error en la solicitud POST:', error);
          await this.showToast(
            `Error al guardar la publicación: ${error.error?.message || 'Error desconocido'}`,
            'danger'
          );
          loading.dismiss();
        },
      });
    } catch (error) {
      console.error('Error al procesar la imagen antes de guardar:', error);
      this.showToast(`Error al procesar la imagen: ${error}`, 'danger');
    }
  }

  private base64ToBlob(base64: string, contentType = 'image/png'): Blob {
    try {
      console.log('Convirtiendo Base64 a Blob. Entrada:', base64);
      const [header, data] = base64.split(',');
      if (!header.startsWith('data:image') || !data) {
        console.error('Base64 inválido o sin prefijo:', base64);
        throw new Error('Formato de Base64 inválido.');
      }
      const byteCharacters = atob(data);
      const byteNumbers = Array.from(byteCharacters, (char) => char.charCodeAt(0));
      const byteArray = new Uint8Array(byteNumbers);
      return new Blob([byteArray], { type: contentType });
    } catch (error) {
      console.error('Error al convertir Base64 a Blob:', error);
      throw new Error('Formato de Base64 inválido.');
    }
  }

  async applyFilterToPhoto(filter: { name: string; value: string }) {
    if (!this.photo) {
      this.showToast('No hay foto para aplicar el filtro.', 'danger');
      return;
    }

    const loading = await this.loadingController.create({
      message: `Aplicando ${filter.name}...`,
    });
    await loading.present();

    const formData = new FormData();
    formData.append('filter_type', filter.value);
    formData.append('num_threads', '1024');
    formData.append('mask_size', '3');
    formData.append('rutaImagen', this.photo!);

    this.http.post(`${this.baseUrl}/apply_filter`, formData).subscribe({
      next: (response: any) => {
        console.log('Respuesta del filtro aplicado:', response);

        // Completar la URL en el frontend
        const processedImageName = response.processed_image_url;
        this.filteredPhoto = `${this.baseUrl}/uploads/${processedImageName}`;
        this.displayPhoto = this.filteredPhoto;
        this.showOriginal = false;

        this.showToast('Filtro aplicado correctamente.', 'success');
        loading.dismiss();
      },
      error: (error) => {
        console.error('Error al aplicar el filtro:', error);
        this.showToast(
          `Error al aplicar el filtro: ${error.error?.message || 'Error desconocido'}`,
          'danger'
        );
        loading.dismiss();
      },
    });
  }


  discardPhoto() {
    console.log('Descartando foto y navegando a la página principal.');
    this.router.navigate(['/tabs/home']);
  }
}
