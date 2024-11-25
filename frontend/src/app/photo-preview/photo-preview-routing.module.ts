import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { PhotoPreviewPage } from './photo-preview.page';

const routes: Routes = [
  {
    path: '',
    component: PhotoPreviewPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PhotoPreviewPageRoutingModule {}
