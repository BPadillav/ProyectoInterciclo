import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-comments',
  templateUrl: './comments.page.html',
  styleUrls: ['./comments.page.scss'],
})
export class CommentsPage implements OnInit {
  comments: any[] = [];
  postId: string | null = null;
  newReply: string = ''; // Almacena la respuesta nueva

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    // Obtiene el ID del post desde la ruta
    this.postId = this.route.snapshot.paramMap.get('postId');

    if (this.postId) {
      this.loadComments(this.postId);
    }
  }

  loadComments(postId: string) {
    this.http.get<any>('assets/data/comments.json').subscribe((data) => {
      this.comments = data[postId] || [];
    });
  }

  toggleReply(comment: any) {
    // Activa o desactiva el campo de respuesta
    comment.isReplying = !comment.isReplying;
  }

  addReply(comment: any) {
    if (this.newReply.trim()) {
      comment.replies.push({
        username: 'your_username',
        avatar: 'assets/img/avatars/7.jpg',
        comment: this.newReply,
        time: 'Justo ahora',
        likes: 0,
      });
      this.newReply = ''; // Resetea el campo de respuesta
      comment.isReplying = false; // Oculta el campo de respuesta
    }
  }
}
