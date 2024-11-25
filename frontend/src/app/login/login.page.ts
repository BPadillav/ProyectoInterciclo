import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  email: string = '';
  password: string = '';

  constructor(private router: Router) {}

  ngOnInit() {
  }

  login() {
    // Simulación de autenticación (esto se conecta con un backend real más adelante)
    if (this.email === 'root' && this.password === 'root') {
      localStorage.setItem('authToken', 'fake-token'); // Almacena un token falso en localStorage
      this.router.navigate(['/tabs/home']); // Redirige a la página principal
    } else {
      alert('Credenciales incorrectas');
    }
  }

}
