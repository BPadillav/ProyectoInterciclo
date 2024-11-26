import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ToastController } from '@ionic/angular';

@Component({
  selector: 'app-comments',
  templateUrl: './comments.page.html',
  styleUrls: ['./comments.page.scss'],
})
export class CommentsPage implements OnInit {
  comments: any[] = [];
  postId: string | null = null;
  newComment: string = ''; // Almacena un nuevo comentario
  private baseUrl: string = ''; // Cargado desde el localStorage
  user: any | null = null;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private toastController: ToastController
  ) {}

  ngOnInit() {
    // Obtiene la URL base desde localStorage o usa el valor por defecto
    this.baseUrl = localStorage.getItem('serverUrl') || 'http://localhost:5000';
    this.user = JSON.parse(localStorage.getItem('authToken') || '{}');


    // Obtiene el ID del post desde la ruta
    this.postId = this.route.snapshot.paramMap.get('postId');

    if (this.postId) {
      this.loadComments(this.postId);
    }
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

  loadComments(postId: string) {
    this.http.get<any[]>(`${this.baseUrl}/list_comments/${postId}`).subscribe({
      next: (data) => {
        this.comments = data || [];
      },
      error: (err) => {
        console.error('Error al cargar comentarios:', err);
        this.showToast('No se pudieron cargar los comentarios', 'danger');
      },
    });
  }

  addComment() {
    if (this.newComment.trim()) {
      const commentData = {
        publicIDComment: this.postId,
        contenido: this.newComment,
        username: this.user.username,
        userIDComment: this.user.IDuser,
      };

      console.log(commentData);
      console.log(this.user);
      
      this.http.post(`${this.baseUrl}/create_comment`, commentData).subscribe({
        next: (response: any) => {
          this.showToast('Comentario agregado', 'success');
          this.comments.push({
            ...commentData,
            time: 'Justo ahora',
            likes: 0,
            avatar: this.user.avatar,
            replies: [],
          });
          this.newComment = ''; // Limpia el campo
        },
        error: (err) => {
          console.error('Error al agregar comentario:', err);
          this.showToast('No se pudo agregar el comentario', 'danger');
        },
      });
    }
  }

  toggleReply(comment: any) {
    comment.isReplying = !comment.isReplying;

    if (!comment.newReply) {
      comment.newReply = '';
    }
  }

  addReply(comment: any) {
    if (comment.newReply.trim()) {
      const replyData = {
        commentId: comment.id, // Usa el ID del comentario padre
        reply: comment.newReply,
        username: 'your_username',
      };

      this.http.post(`${this.baseUrl}/replies`, replyData).subscribe({
        next: (response: any) => {
          this.showToast('Respuesta agregada', 'success');
          comment.replies = comment.replies || [];
          comment.replies.push({
            ...replyData,
            time: 'Justo ahora',
            likes: 0,
            avatar: 'assets/img/avatars/7.jpg',
          });
          comment.newReply = ''; // Limpia el campo de respuesta
          comment.isReplying = false; // Cierra el campo de respuesta
        },
        error: (err) => {
          console.error('Error al agregar respuesta:', err);
          this.showToast('No se pudo agregar la respuesta', 'danger');
        },
      });
    }
  }
}
