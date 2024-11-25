import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.scss'],
})
export class ProfilePage implements OnInit {
  profile: any = {}; // Información del perfil
  posts: any[] = []; // Publicaciones del perfil

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadProfile();
    this.loadPosts();
  }

  loadProfile() {
    this.http.get<any>('assets/data/profile.json').subscribe((data) => {
      this.profile = data;
    });
  }

  loadPosts() {
    this.http.get<any[]>('assets/data/posts.json').subscribe((data) => {
      this.posts = data.map((post) => ({
        image: post.image,
      }));
    });
  }

  logout() {
    // Elimina el token de autenticación
    localStorage.removeItem('authToken');
    // Redirige al usuario a la página de inicio de sesión
    this.router.navigate(['/login']);
  }
}
