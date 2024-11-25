import { CanActivateFn } from '@angular/router';
import { inject } from '@angular/core';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router); // Inyecta el servicio de Router
  const isAuthenticated = !!localStorage.getItem('authToken'); // Comprueba si hay un token en localStorage

  if (!isAuthenticated) {
    router.navigate(['/login']); // Redirige al usuario al login si no está autenticado
    return false;
  }

  return true; // Permite el acceso si el usuario está autenticado
};
