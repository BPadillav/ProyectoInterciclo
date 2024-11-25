import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'home',
        loadChildren: () => import('../home/home.module').then(m => m.HomePageModule),
      },
      {
        path: 'comments/:postId', // Ruta dinámica
        loadChildren: () =>
          import('../comments/comments.module').then((m) => m.CommentsPageModule),
      },
      {
        path: 'camera',
        loadChildren: () => import('../camera/camera.module').then(m => m.CameraPageModule),
      },
      // {
      //   path: 'reels',
      //   loadChildren: () => import('../reels/reels.module').then(m => m.ReelsPageModule),
      // },
      // {
      //   path: 'shop',
      //   loadChildren: () => import('../shop/shop.module').then(m => m.ShopPageModule),
      // },
      {
        path: 'profile',
        loadChildren: () => import('../profile/profile.module').then(m => m.ProfilePageModule),
      },
      {
        path: 'photo-preview',
        loadChildren: () => import('../photo-preview/photo-preview.module').then( m => m.PhotoPreviewPageModule)
      },
      {
        path: '',
        redirectTo: '/tabs/home',
        pathMatch: 'full',
      },


    ],

  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TabsPageRoutingModule { }
