import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.page.html',
  styleUrls: ['./camera.page.scss'],
})
export class CameraPage implements OnInit, OnDestroy {
  @ViewChild('cameraPreview', { static: false }) cameraPreview!: ElementRef<HTMLVideoElement>;

  photo: string | undefined; // URL o base64 de la foto seleccionada
  private stream: MediaStream | undefined; // Stream de la cámara
  private cameraFacing: 'user' | 'environment' = 'environment'; // Dirección de la cámara
  mode: 'publicacion' | 'historia' = 'historia'; // Modo de la cámara

  constructor(private navCtrl: NavController) {}

  async ngOnInit() {
    // Verificar y solicitar permisos al iniciar
    await this.checkCameraPermissions();
  }

  ionViewWillEnter() {
    this.photo = undefined;
    this.startCamera();
  }

  ionViewWillLeave() {
    this.stopCamera();
  }

  ngOnDestroy() {
    this.stopCamera();
  }

  // Verificar permisos de cámara
  async checkCameraPermissions() {
    const permissions = await Camera.checkPermissions();

    if (permissions.camera !== 'granted') {
      const request = await Camera.requestPermissions({ permissions: ['camera'] });

      if (request.camera !== 'granted') {
        console.error('Permiso de cámara denegado');
        this.navCtrl.navigateBack('/tabs/home'); // Redirigir si no hay permiso
        return;
      }
    }
  }

  async startCamera() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: this.cameraFacing,
        },
      });

      if (this.cameraPreview && this.cameraPreview.nativeElement) {
        this.cameraPreview.nativeElement.srcObject = this.stream;
      }
    } catch (error) {
      console.error('Error al acceder a la cámara:', error);
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
      this.stream = undefined;
    }
  }

  async takePhoto() {
    const canvas = document.createElement('canvas');
    const video = this.cameraPreview.nativeElement;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');
    if (context) {
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.photo = canvas.toDataURL('image/png'); // Captura la imagen como base64

      // Navega a la página de previsualización
      this.navCtrl.navigateForward('tabs/photo-preview', {
        queryParams: { photo: this.photo },
      });
    }

    this.stopCamera();
  }

  async selectPhoto() {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: true,
        resultType: CameraResultType.DataUrl,
        source: CameraSource.Photos,
      });

      this.photo = image.dataUrl;
      this.stopCamera();

      // Navega a la página de previsualización
      this.navCtrl.navigateForward('tabs/photo-preview', {
        queryParams: { photo: this.photo },
      });
    } catch (error) {
      console.error('Error al seleccionar foto:', error);
    }
  }

  switchCamera() {
    this.cameraFacing = this.cameraFacing === 'user' ? 'environment' : 'user';
    this.stopCamera();
    this.startCamera();
  }

  switchMode(event: any) {
    this.mode = event.detail.value;
  }

  exitCamera() {
    this.photo = undefined;
    this.stopCamera();
    this.navCtrl.navigateBack('/tabs/home'); // Regresa a la página principal
  }
}
