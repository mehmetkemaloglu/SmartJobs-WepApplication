import { Component, OnInit } from '@angular/core';
import { LoginService } from '../login.service';
import { Router } from '@angular/router';
import { EventEmitterService } from '../event-emitter.service';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.scss']
})
export class TopBarComponent implements OnInit {
  

  constructor(
    private loginService:LoginService,
    private router: Router,
    private eventEmitterService: EventEmitterService) { }

  ngOnInit() {
  }
  
  logOut(){
    this.loginService.logOut();
    this.eventEmitterService.onFirstComponentButtonClick(); 
    this.router.navigate(['/login']);
  }

  routeMainPageByLogo(){
    if(this.loginService.loggedIn()){
      this.router.navigate(['/inbox']);
    }
    else{
      this.router.navigate(['/search']);
    }
  }
  isLoggedIn(){
    return this.loginService.loggedIn();
  }
}
