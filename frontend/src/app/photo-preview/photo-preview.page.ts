import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-photo-preview',
  templateUrl: './photo-preview.page.html',
  styleUrls: ['./photo-preview.page.scss'],
})
export class PhotoPreviewPage implements OnInit {
  photo: string | undefined; // Foto original
  filteredPhoto: string | undefined; // Foto con filtro aplicado
  displayPhoto: string | undefined; // Foto actualmente mostrada (original o filtrada)
  showOriginal: boolean = true; // Estado para alternar entre original y filtro

  filters = [
    { name: 'Filtro 1', value: 'filter1' },
    { name: 'Filtro 2', value: 'filter2' },
    { name: 'Filtro 3', value: 'filter3' },
  ]; // Filtros disponibles

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      this.photo = params['photo'];
      this.displayPhoto = this.photo; // Inicialmente mostrar la foto original
    });
  }

  applyFilter(filter: { name: string; value: string }) {
    if (!this.photo) return;
  
    // Simula una URL dinámica basada en el filtro
    const simulatedServerResponse = `https://via.placeholder.com/600x400?text=${encodeURIComponent(filter.name)}`;
  
    this.filteredPhoto = simulatedServerResponse; // Obtén la URL simulada
    this.displayPhoto = this.filteredPhoto; // Muestra la foto con el filtro aplicado
    this.showOriginal = false; // Cambia al estado de mostrar el filtro
    console.log(`Filtro aplicado: ${filter.name}, URL simulada: ${simulatedServerResponse}`);
  }
  

  toggleOriginal() {
    this.showOriginal = !this.showOriginal; // Alterna entre mostrar original y filtro
    this.displayPhoto = this.showOriginal ? this.photo : this.filteredPhoto;
  }

  savePhoto() {
    console.log('Foto guardada:', this.filteredPhoto || this.photo);
    this.router.navigate(['/tabs/home']);
  }

  discardPhoto() {
    this.router.navigate(['/tabs/home']);
  }
}
