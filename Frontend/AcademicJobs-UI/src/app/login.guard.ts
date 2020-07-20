import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { LoginService } from './login.service';

@Injectable({
  providedIn: 'root'
})
export class LoginGuard implements CanActivate{
  /*
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return true;
  }*/
  constructor(
    private loginService:LoginService,
    private router: Router
  ){

  }
  canActivate(): boolean {
    //return true;
    if (this.loginService.loggedIn()){
      return true;
    }
    else{
      this.router.navigate(['/login']);
      return false;
    }
  }

  
}
