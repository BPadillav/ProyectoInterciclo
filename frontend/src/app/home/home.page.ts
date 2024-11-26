import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
})
export class HomePage implements OnInit {
  stories: any[] = [];
  posts: any[] = [];
  private baseUrl: string = 'http://localhost:5000';

  constructor(private http: HttpClient, private router: Router) {}

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
        avatar: `${this.baseUrl}/uploads/${encodeURIComponent(post.avatar.replace('./uploads/', ''))}?t=${new Date().getTime()}`,
        image: `${this.baseUrl}/uploads/${encodeURIComponent(post.image.replace('./uploads/', ''))}?t=${new Date().getTime()}`,
        comments : []
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
}
