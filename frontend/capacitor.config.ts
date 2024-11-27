import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'io.ionic.starter',
  appName: 'instagramClone',
  webDir: 'www',
  server: {
    cleartext: true,
    allowNavigation: ['*'], // Permitir cualquier dominio
    androidScheme: 'http'
  }
};

export default config;
