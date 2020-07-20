import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import {MatIconModule} from '@angular/material/icon';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { CalendarUtilsModule } from './calendar-utils/module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TopBarComponent } from './top-bar/top-bar.component';
import { InboxComponent } from './inbox/inbox.component';
import { SearchComponent } from './search/search.component';
import { LikedComponent } from './liked/liked.component';
import { LabeledComponent } from './labeled/labeled.component';
import { SecondBarComponent } from './second-bar/second-bar.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { CalendarContainerComponent } from './calendar-container/calendar-container.component';
import { SearchQueriesComponent } from './search-queries/search-queries.component';
import { JobPageComponent } from './job-page/job-page.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { LoginGuard } from './login.guard';
import { WantToApplyComponent } from './want-to-apply/want-to-apply.component';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { EventEmitterService } from './event-emitter.service';

@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    InboxComponent,
    SearchComponent,
    LikedComponent,
    LabeledComponent,
    SecondBarComponent,
    PageNotFoundComponent,
    CalendarContainerComponent,
    SearchQueriesComponent,
    JobPageComponent,
    LoginComponent,
    SignupComponent,
    WantToApplyComponent
  ],
  imports: [
    BrowserModule,  
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatIconModule,
    BrowserAnimationsModule,
    RouterModule.forRoot([
      {
        path: '',
        redirectTo: '/search',
        pathMatch: 'full'
      },
      { path: 'login', component: LoginComponent },
      { path: 'signup', component: SignupComponent },
      { path: 'job-page', component: JobPageComponent },
      { path: 'job-page/:jid', component: JobPageComponent },
      { path: 'inbox', component: InboxComponent, canActivate: [LoginGuard]  },
      { path: 'search', component: SearchComponent },
      { path: 'search/keyword/:keyword/location/:country/field/:field/jobType/:jobType', component: SearchComponent},
      { path: 'search/keyword/:keyword', component: SearchComponent},
      { path: 'liked', component: LikedComponent, canActivate: [LoginGuard]  },
      { path: 'want-to-apply', component: WantToApplyComponent, canActivate: [LoginGuard]  },
      { path: 'labeled', component: LabeledComponent, canActivate: [LoginGuard] },
      { path: 'saved-queries', component: SearchQueriesComponent, canActivate: [LoginGuard] },
      { path: '**', component: PageNotFoundComponent },
     
  
    ]),
    CalendarModule.forRoot({ provide: DateAdapter, useFactory: adapterFactory }),
    CalendarUtilsModule
  ],
  providers: [EventEmitterService],
  bootstrap: [AppComponent]
})
export class AppModule { }
