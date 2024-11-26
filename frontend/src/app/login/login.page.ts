import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastController, AlertController } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  email: string = '';
  password: string = '';
  private baseUrl: string = localStorage.getItem('serverUrl') || 'http://localhost:5000'; // Obtiene la IP desde localStorage o usa el valor por defecto

  constructor(
    private http: HttpClient,
    private toastController: ToastController,
    private alertController: AlertController,
    private router: Router
  ) { }

  ngOnInit() { }

  async showToast(message: string, color: string = 'dark') {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      position: 'bottom',
      color,
    });
    await toast.present();
  }

  async configureServerUrl() {
    const alert = await this.alertController.create({
      header: 'Configurar Servidor',
      inputs: [
        {
          name: 'serverUrl',
          type: 'text',
          placeholder: 'http://localhost:5000',
          value: this.baseUrl, // Usa el valor actual como valor por defecto
        },
      ],
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
        },
        {
          text: 'Guardar',
          handler: (data) => {
            if (data.serverUrl) {
              this.baseUrl = data.serverUrl;
              localStorage.setItem('serverUrl', this.baseUrl); // Guarda la IP en localStorage
              this.showToast('Servidor actualizado', 'success');
            }
          },
        },
      ],
    });
    await alert.present();
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
          localStorage.setItem('authToken', JSON.stringify(response));
          this.showToast('Inicio de sesión exitoso', 'success');
          this.router.navigate(['/tabs/home']);
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
