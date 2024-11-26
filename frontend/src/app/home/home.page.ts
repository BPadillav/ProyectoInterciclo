import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
})
export class HomePage implements OnInit {
  stories: any[] = [];
  posts: any[] = [];
  private baseUrl: string = '';
  private user: any = null;

  constructor(
    private http: HttpClient,
    private toastController: ToastController,
    private router: Router
  ) {}

  ngOnInit() {
    // Cargar la baseUrl desde localStorage o usar valor por defecto
    this.baseUrl = localStorage.getItem('serverUrl') || 'http://localhost:5000';
    const authToken = localStorage.getItem('authToken') || '{}'; // Proveer valor predeterminado
    this.user = JSON.parse(authToken);
    this.loadStories();
    this.loadPosts();
  }

  ionViewWillEnter() {
    this.loadStories();
    this.loadPosts();
  }

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000, // 2 segundos
      position: 'bottom',
      color, // Puedes usar colores como 'success', 'danger', 'warning', etc.
    });
    await toast.present();
  }

  loadStories() {
    this.http.get<any[]>('assets/data/stories.json').subscribe((data) => {
      this.stories = data;
    });
  }

  loadPosts() {
    this.http.get<any[]>(`${this.baseUrl}/list_publicaciones`).subscribe((data) => {
      this.posts = data.map(post => ({
        ...post,
        avatar: `${this.baseUrl}/uploads/${encodeURIComponent(post.rutaImagen.replace('./uploads/', ''))}?t=${new Date().getTime()}`,
        rutaImagen: `${this.baseUrl}/uploads/${encodeURIComponent(post.rutaImagen.replace('./uploads/', ''))}?t=${new Date().getTime()}`,
      }));
      console.log('Posts cargados:', this.posts);
    });
  }

  onImageError(event: Event) {
    const element = event.target as HTMLImageElement;
    element.src = 'assets/default-image.png'; // Imagen predeterminada
  }

  viewComments(postId: number) {
    console.log(`Navegando a los comentarios del post con ID: ${postId}`);
    this.router.navigate(['/tabs/comments', postId]);
  }

  likePost(postId: number, post: any) {
  const body = {
    userIDLike: this.user.IDuser, // ID del usuario que da el like
    publicIDLike: postId // Asume que estás dando like a una publicación
  };

  console.log(this.user);
  

  this.http.post(`${this.baseUrl}/create_like`, body).subscribe({
    next: (response: any) => {
      console.log('Like registrado:', response);
      post.likes += 1; // Incrementar los likes en el frontend
      this.showToast('¡Te gustó esta publicación!', 'success');
    },
    error: (err) => {
      console.error('Error al registrar el like:', err);
      this.showToast('No se pudo registrar el like. Intenta de nuevo.', 'danger');
    }
  });
}

}
