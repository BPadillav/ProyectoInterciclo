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
    this.http.get<any>(`${this.baseUrl}/comments/${postId}`).subscribe({
      next: (data) => {
        this.comments = data[postId] || []; // Extrae los comentarios del postId específico
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

      // console.log(commentData);
      // console.log(this.user);
      
      this.http.post(`${this.baseUrl}/create_comment`, commentData).subscribe({
        next: (response: any) => {
          this.showToast('Comentario agregado', 'success');
          // this.comments.push({
          //   ...commentData,
          //   time: 'Justo ahora',
          //   likes: 0,
          //   avatar: this.user.avatar,
          //   replies: [],
          // });
          this.loadComments(this.postId!);
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
        commentIDAnswer: comment.IDcomments, // ID del comentario padre
        contenido: comment.newReply, // Contenido de la respuesta
        userIDAnswer: this.user.IDuser, // ID del usuario que responde
      };
  
      this.http.post(`${this.baseUrl}/create_answer`, replyData).subscribe({
        next: (response: any) => {
          this.showToast('Respuesta agregada', 'success');
  
          // Agregar la nueva respuesta al comentario
          comment.replies = comment.replies || [];
          this.loadComments(this.postId!);
  
          // Limpiar el campo de respuesta
          comment.newReply = '';
          comment.isReplying = false;
        },
        error: (err) => {
          console.error('Error al agregar respuesta:', err);
          this.showToast('No se pudo agregar la respuesta', 'danger');
        },
      });
    }
  }


  likeComment(comment: any) {
    const body = {
      userIDLike: this.user.IDuser, // ID del usuario que da el like
      commentIDLike: comment.IDcomments, // ID del comentario que recibe el like
    };
  
    this.http.post(`${this.baseUrl}/like_comment`, body).subscribe({
      next: (response: any) => {
        console.log('Like al comentario registrado:', response);
        comment.likes += 1; // Incrementar el contador de likes en el comentario
        this.showToast('¡Te gustó este comentario!', 'success');
      },
      error: (err) => {
        console.error('Error al dar like al comentario:', err);
        this.showToast('No se pudo registrar el like. Intenta de nuevo.', 'danger');
      }
    });
  }
  
  likeReply(reply: any) {
    const body = {
      userIDLike: this.user.IDuser, // ID del usuario que da el like
      answerIDLike: reply.IDanswer, // ID de la respuesta que recibe el like
    };
  
    this.http.post(`${this.baseUrl}/like_comment`, body).subscribe({
      next: (response: any) => {
        console.log('Like a la respuesta registrado:', response);
        reply.likes += 1; // Incrementar el contador de likes en la respuesta
        this.showToast('¡Te gustó esta respuesta!', 'success');
      },
      error: (err) => {
        console.error('Error al dar like a la respuesta:', err);
        this.showToast('No se pudo registrar el like. Intenta de nuevo.', 'danger');
      }
    });
  }
  
  
}
