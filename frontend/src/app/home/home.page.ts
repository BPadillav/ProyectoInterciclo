import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router'; // Importamos Router para manejar la navegación

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
})
export class HomePage implements OnInit {
  stories: any[] = [];
  posts: any[] = [];
  private baseUrl: string = 'http://localhost:5000'; // Cambia esta URL si está en producción

  constructor(private http: HttpClient, private router: Router) {} // Agregamos Router al constructor

  ngOnInit() {
    this.loadStories();
    this.loadPosts();
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
        avatar: `${this.baseUrl}/uploads/${post.avatar.replace('./uploads/', '')}`, // Construir la URL completa
      image: `${this.baseUrl}/uploads/${post.image.replace('./uploads/', '')}`   // Construir la URL completa
      }));
    });
  }
  

  viewComments(postId: number) {
    console.log(`Navegando a los comentarios del post con ID: ${postId}`);
    this.router.navigate(['/tabs/comments', postId]); // Navegamos a la ruta dinámica
  }


}
