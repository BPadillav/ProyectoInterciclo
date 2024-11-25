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
    this.http.get<any[]>('assets/data/posts.json').subscribe((data) => {
      this.posts = data;
    });
  }

  viewComments(postId: number) {
    console.log(`Navegando a los comentarios del post con ID: ${postId}`);
    this.router.navigate(['/tabs/comments', postId]); // Navegamos a la ruta dinámica
  }


}
