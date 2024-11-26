import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-photo-preview',
  templateUrl: './photo-preview.page.html',
  styleUrls: ['./photo-preview.page.scss'],
})
export class PhotoPreviewPage implements OnInit {
  photo: string | undefined; // Foto original en Base64
  filteredPhoto: string | undefined; // Foto con filtro aplicado
  displayPhoto: string | undefined; // Foto actualmente mostrada (original o filtrada)
  showOriginal: boolean = true; // Estado para alternar entre original y filtro
  private baseUrl: string = 'http://localhost:5000'; // Cambia esta URL si está en producción

  filters = [
    { name: 'Filtro 1', value: 'filter1' },
    { name: 'Filtro 2', value: 'filter2' },
    { name: 'Filtro 3', value: 'filter3' },
  ]; // Filtros disponibles

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private toastController: ToastController
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      this.photo = params['photo'];
      this.displayPhoto = this.photo; // Inicialmente mostrar la foto original
    });
  }

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000, // 2 segundos
      position: 'bottom',
      color, // Colores: 'success', 'danger', etc.
    });
    await toast.present();
  }

  applyFilter(filter: { name: string; value: string }) {
    if (!this.photo) return;

    const simulatedServerResponse = `https://via.placeholder.com/600x400?text=${encodeURIComponent(filter.name)}`;
    this.filteredPhoto = simulatedServerResponse; // Simula una foto filtrada
    this.displayPhoto = this.filteredPhoto;
    this.showOriginal = false; // Cambia al estado de mostrar el filtro
  }

  toggleOriginal() {
    this.showOriginal = !this.showOriginal;
    this.displayPhoto = this.showOriginal ? this.photo : this.filteredPhoto;
  }

  private base64ToBlob(base64: string, contentType = 'image/png'): Blob {
    const byteCharacters = atob(base64.split(',')[1]);
    const byteNumbers = Array.from(byteCharacters, (char) => char.charCodeAt(0));
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
  }

  async savePhoto() {
    if (!this.filteredPhoto && !this.photo) {
      this.showToast('No hay foto para guardar.', 'danger');
      return;
    }

    // Crear un objeto FormData para enviar datos al backend
    const formData = new FormData();
    formData.append('userIDPublic', '1'); // ID del usuario
    formData.append('contenido', 'Descripción de la foto'); // Contenido o descripción
    formData.append('filtroIDPublic', '1'); // ID del filtro aplicado

    // Convertir la imagen a Blob y añadirla al FormData
    const base64Photo = this.filteredPhoto || this.photo;
    if (base64Photo) {
      const photoBlob = this.base64ToBlob(base64Photo);
      formData.append('rutaImagen', photoBlob, 'photo.png'); // Añadir el archivo
    } else {
      this.showToast('Error al procesar la imagen.', 'danger');
      return;
    }

    // Realizar la solicitud POST directamente
    this.http.post(`${this.baseUrl}/create_publicacion`, formData).subscribe({
      next: async () => {
        await this.showToast('Publicación creada exitosamente.', 'success');
        this.router.navigate(['/tabs/home']);
      },
      error: async (error) => {
        await this.showToast(
          `Error al guardar la publicación: ${error.error.message || 'Error desconocido'}`,
          'danger'
        );
      },
    });
  }

  discardPhoto() {
    this.router.navigate(['/tabs/home']);
  }
}
