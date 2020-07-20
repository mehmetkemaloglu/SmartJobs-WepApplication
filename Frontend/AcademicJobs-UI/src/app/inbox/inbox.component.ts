import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, Router } from '@angular/router';

import tooltipData from '../../assets/tooltipDescription.json';
@Component({
  selector: 'app-inbox',
  templateUrl: './inbox.component.html',
  styleUrls: ['./inbox.component.scss']
})
export class InboxComponent implements OnInit {
  jobs;
  loading="";
  //paging variables
  viewedQueries;
  currentPage=1;
  numOfItemsInPage=10;
  pageNum: number;
  nums=[];
  //tooltip
  tooltip;

  constructor(private userService: UserService,
    private router: Router) {
      this.tooltip=tooltipData.inbox;
   }

  ngOnInit() {
    this.getJobs();
  }

  getJobs(){
    this.loading="Loading..."
    this.userService.getInbox()
      .subscribe( res=>{
        this.jobs=res;
        this.loading="";
        this.pageNum=Math.ceil(this.jobs.length/this.numOfItemsInPage);
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );
  }
  
  goToJobSite(job){
    this.userService.currentJob=job;
    this.router.navigate(['/job-page/'+job.jid]);
  }

  selectPage(i){
    this.currentPage=i;
    this.getviewedQueriesByPage();
  }

  getviewedQueriesByPage(){
    this.viewedQueries=[];
    for (let i = (this.currentPage-1)*this.numOfItemsInPage;i<(this.currentPage)*this.numOfItemsInPage;i++){
      if (!this.jobs[i]){
        break;
      }
      this.viewedQueries.push(this.jobs[i]);
    } 
  }
}
