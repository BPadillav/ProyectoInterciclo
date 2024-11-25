import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { PhotoPreviewPageRoutingModule } from './photo-preview-routing.module';

import { PhotoPreviewPage } from './photo-preview.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    PhotoPreviewPageRoutingModule
  ],
  declarations: [PhotoPreviewPage]
})
export class PhotoPreviewPageModule {}
