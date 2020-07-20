import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { colors } from '../calendar-utils/colors';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

import {
  ViewChild,
  TemplateRef,
} from '@angular/core';
import {
  startOfDay,
  endOfDay,
  subDays,
  addDays,
  endOfMonth,
  isSameDay,
  isSameMonth,
  addHours,
} from 'date-fns';
import { Subject } from 'rxjs';

import {
  CalendarEventAction,
  CalendarEventTimesChangedEvent,
} from 'angular-calendar';
import { LoginService } from '../login.service';
import { EventEmitterService } from '../event-emitter.service';

@Component({
  selector: 'app-calendar-container',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './calendar-container.component.html',
  styleUrls: ['./calendar-container.component.scss']
})
export class CalendarContainerComponent implements OnInit {
  
  wantToApply;

  constructor(private userService: UserService,
    private loginService: LoginService,
    private router: Router,
    private eventEmitterService: EventEmitterService
    ) {
      
      
  }

  ngOnInit() {
    if(this.loginService.loggedIn()){
      this.getSavedJobs();
    }
    else{
      this.events=[];
      this.refresh.next();
    } 
    if (this.eventEmitterService.subsVar==undefined) {    
      this.eventEmitterService.subsVar = this.eventEmitterService.    
      invokeFirstComponentFunction.subscribe((name:string) => {    
        if(this.loginService.loggedIn()){
          this.getSavedJobs();
        }
        else{
          this.events=[];
          this.refresh.next();
        } 
      });    
    }    
  }

  getSavedJobs(){
    this.userService.getSavedJobs()
      .subscribe( res=>{
        let labeledJobs=res;
        this.wantToApply=this.getWantToApply(labeledJobs);
        console.log(this.wantToApply);
        if (!this.wantToApply){
        }
        else{
          this.addAllEvents();
        }
        this.refresh.next();
        },
        err=>{
          console.log(err);
        }
      );

  }

  getWantToApply(labeledJobs){
    let want=[];
    for(let i=0;i<labeledJobs.length;i++){
      if(labeledJobs[i].label=="Want to Apply" && labeledJobs[i].deadline!="Unspecified"){ 
        let temp = new Date(Date.parse(labeledJobs[i].deadline));
        labeledJobs[i].deadline=this.formatDate(temp); 
        want.push(labeledJobs[i]);
      }
    }
    return want;

  }


  formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

  view: CalendarView = CalendarView.Month;

  viewDate: Date = new Date();

  events: CalendarEvent[] = [];

  refresh: Subject<any> = new Subject();
  
  activeDayIsOpen: boolean = false;

  //constructor(private modal: NgbModal) {}

  dayClicked({ date, events }: { date: Date; events: CalendarEvent[] }): void {
    if (isSameMonth(date, this.viewDate)) {
      if (
        (isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
        events.length === 0
      ) {
        this.activeDayIsOpen = false;
      } else {
        this.activeDayIsOpen = true;
      }
      this.viewDate = date;
    }
  }

  handleEvent(action: string, event: CalendarEvent): void {
    console.log(this.wantToApply);
    console.log(event);
    for (let i=0;i<this.wantToApply.length;i++){
      if (this.wantToApply[i].name===event.title){
        this.router.navigate(['/job-page/'+this.wantToApply[i].jid]);
      }
    }
  }

  addEvent(title_,date_): void {
    this.events = [
      ...this.events,
      {
        title: title_,
        start: new Date(date_),
        end: new Date(date_),
        color: colors.red,
        draggable: false,
        resizable: {
          beforeStart: false,
          afterEnd: false,
        },
      },
    ];
  }

  addAllEvents(){
    this.events=[];
    for (let i=0;i<this.wantToApply.length;i++){
      this.addEvent(this.wantToApply[i].name,this.wantToApply[i].deadline);
    }
  }

}
