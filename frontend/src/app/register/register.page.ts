import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  fullName: string = '';
  username: string = '';

  private baseUrl: string = 'http://192.168.18.83:5000'; // Cambia esta URL si está en producción

  constructor(private http: HttpClient, private toastController: ToastController,private router: Router) { }

  ngOnInit() {}

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000, // 2 segundos
      position: 'bottom',
      color, // Puedes usar colores como 'success', 'danger', 'warning', etc.
    });
    await toast.present();
  }

  register() {
    if (this.password !== this.confirmPassword) {
      this.showToast('Las contraseñas no coinciden', 'danger');
      return;
    }

    const userData = {
      email: this.email,
      password: this.password,
      fullname: this.fullName,
      username: this.username,
      avatar: null // O maneja lógicamente el avatar si lo necesitas
    };

    this.http.post(`${this.baseUrl}/create_user`, userData).subscribe({
      next: (response: any) => {
        if (response.valid == 'true') {
          this.showToast('Registro exitoso', 'success');
          this.router.navigate(['/login']); // Redirige a la página principal
        } else {
          this.showToast(response.message, 'danger');
        }
        // console.log('Usuario registrado:', response);
        
      },
      error: (err) => {
        // console.error('Error al registrar:', err);
        this.showToast('Ocurrió un error al registrar el usuario:' +err.error.message, 'danger');
      }
    });
    
  }
}
