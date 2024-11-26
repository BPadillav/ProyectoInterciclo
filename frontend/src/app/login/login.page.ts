import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  email: string = '';
  password: string = '';
  private baseUrl: string = 'http://localhost:5000'; // Cambia esta URL si está en producción

  constructor(
    private http: HttpClient,
    private toastController: ToastController,
    private router: Router
  ) { }

  ngOnInit() { }

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000, // 2 segundos
      position: 'bottom',
      color, // Puedes usar colores como 'success', 'danger', 'warning', etc.
    });
    await toast.present();
  }

  login() {
    if (!this.email || !this.password) {
      this.showToast('Correo electrónico y contraseña son requeridos', 'danger');
      return;
    }

    const loginData = {
      email: this.email,
      password: this.password,
    };

    this.http.post(`${this.baseUrl}/users/login`, loginData).subscribe({
      next: (response: any) => {
        if (response.valid == 'true') {
          localStorage.setItem('authToken', response.IDuser);
          this.showToast('Inicio de sesión exitoso', 'success');
          this.router.navigate(['/tabs/home']); // Redirige a la página principal
        } else {
          this.showToast(response.message, 'danger');
        }
      },
      error: (err) => {
        console.error('Error al iniciar sesión:', err);
        this.showToast('Credenciales incorrectas', 'danger');
      },
    });
  }
}
