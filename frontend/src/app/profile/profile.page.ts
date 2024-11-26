import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.scss'],
})
export class ProfilePage implements OnInit {
  user: any = {}; // Información del usuario desde localStorage
  profile: any = {
    username: 'Anonymous', // Valor por defecto
    avatar: 'assets/default-avatar.png', // Imagen por defecto
    name: 'Anonymous', // Nombre por defecto
    bio: 'This user has no bio yet.', // Bio por defecto
    website: '', // Valor por defecto
    posts: 0, // Valor por defecto
    followers: 0, // Valor por defecto
    following: 0, // Valor por defecto
  };
  posts: any[] = []; // Publicaciones del perfil
  private baseUrl: string = ''; // Cargado desde el localStorage

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    this.baseUrl = localStorage.getItem('serverUrl') || 'http://localhost:5000';
    this.loadUserFromLocalStorage();
    this.loadProfile();
    this.loadPosts();
  }

  loadUserFromLocalStorage() {
    // Cargar usuario desde localStorage
    this.user = JSON.parse(localStorage.getItem('authToken') || '{}');
    if (!this.user || !this.user.IDuser) {
      console.error('No se encontró información de usuario en localStorage');
      this.router.navigate(['/login']); // Redirigir al login si no hay información del usuario
    }
  }

  loadProfile() {
    // Cargar valores del usuario desde localStorage
    this.profile = {
      username: this.user.username || 'Anonymous',
      avatar: this.user.avatar || 'assets/default-avatar.png',
      name: this.user.name || 'Anonymous',
      bio: this.user.bio || 'This user has no bio yet.',
      website: this.user.website || '',
      posts: this.user.posts || 0,
      followers: this.user.followers || 0,
      following: this.user.following || 0,
    };
  }

  loadPosts() {
    // Cargar publicaciones utilizando el ID del usuario
    this.http.get<any[]>(`${this.baseUrl}/posts_with_comments?user_id=${this.user.IDuser}`).subscribe(
      (data) => {
        this.posts = data.map((post) => ({
          image: post.rutaImagen || 'assets/default-post.png', // Imagen por defecto
        }));
      },
      (error) => {
        console.error('Error al cargar publicaciones:', error);
        this.posts = []; // Si ocurre un error, se deja vacío
      }
    );
  }
  logout() {
    // Elimina el token de autenticación
    localStorage.removeItem('authToken');
    // Redirige al usuario a la página de inicio de sesión
    this.router.navigate(['/login']);
  }
}
