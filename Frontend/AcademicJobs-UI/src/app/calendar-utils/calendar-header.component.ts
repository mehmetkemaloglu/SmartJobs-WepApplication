import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CalendarView } from 'angular-calendar';

@Component({
  selector: 'mwl-demo-utils-calendar-header',
  template: `
  
    <div class="row text-center " >
      <div class="col-md-4" >
        <div class="btn-group" 
        style="display:inline-flex;
        color:blue;
        cursor: pointer;
        margin-top:20px;
        margin-left:20px;
        padding-left:130px;
        padding-top:40px;
        font-size:36px;">
          <div 
            class="btn btn-primary"
            mwlCalendarPreviousView
            [view]="view"
            [(viewDate)]="viewDate"
            (viewDateChange)="viewDateChange.next(viewDate)"
          >
            <--Previous
          </div>
          <div
            style="padding-left:50px;"
            class="btn btn-outline-secondary"
            mwlCalendarToday
            [(viewDate)]="viewDate"
            (viewDateChange)="viewDateChange.next(viewDate)"
          >
            Today
          </div>
          <div
          style="padding-left:50px;"
            class="btn btn-primary"
            mwlCalendarNextView
            [view]="view"
            [(viewDate)]="viewDate"
            (viewDateChange)="viewDateChange.next(viewDate)"
          >
            Next-->
          </div>
        </div>
      </div>
      <div class="col-md-4" 
      style="
      font-weight: bold;
      padding-left: 300px;">
        <h3>{{ viewDate | calendarDate: view + 'ViewTitle':locale }}</h3>
      </div>
      
    </div>
    <br />
  `,
})
export class CalendarHeaderComponent {
  @Input() view: CalendarView;

  @Input() viewDate: Date;

  @Input() locale: string = 'en';

  @Output() viewChange = new EventEmitter<CalendarView>();

  @Output() viewDateChange = new EventEmitter<Date>();

  CalendarView = CalendarView;
}
