import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, Router } from '@angular/router';

import tooltipData from '../../assets/tooltipDescription.json';
import { EventEmitterService } from '../event-emitter.service';

@Component({
  selector: 'app-want-to-apply',
  templateUrl: './want-to-apply.component.html',
  styleUrls: ['./want-to-apply.component.scss']
})
export class WantToApplyComponent implements OnInit {

  loading="";
  wantToApply;
  tooltip;
  //paging variables
  viewedQueries;
  currentPage=1;
  numOfItemsInPage=10;
  pageNum: number;
  nums=[];

  constructor(private userService: UserService,
    private router: Router,
    private eventEmitterService: EventEmitterService) { 
     this.tooltip=tooltipData.wantToApply; 
    }

  ngOnInit(): void {
    this.getSavedJobs();
  }

  getSavedJobs(){
    this.loading="Loading..."
    this.userService.getSavedJobs()
      .subscribe( res=>{
        let labeledJobs=res;
        this.wantToApply=this.getWantToApply(labeledJobs);
        console.log(this.wantToApply);
        this.loading="";
        this.pageNum=Math.ceil(this.wantToApply.length/this.numOfItemsInPage);
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        if (!this.wantToApply){
          this.loading="You don't want to apply any job.";
        }
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );

  }

  remove(id){
    this.loading="Deleting..."
    let id_= id+((this.currentPage-1)*this.numOfItemsInPage);
    this.userService.deleteLabelFromJob("Want to Apply",this.wantToApply[id_].jid)
      .subscribe( res=>{
        this.wantToApply.splice(id_, 1);
        this.loading="";
        if (this.wantToApply.length%this.numOfItemsInPage==0){
          console.log("page deleted");
          this.nums.splice(this.nums.length-1,1);
        }
        if (this.wantToApply.length == id_  && id==0 && this.currentPage>1){
          console.log("page changed");
          this.currentPage--;
        }
        this.getviewedQueriesByPage();
        this.eventEmitterService.onFirstComponentButtonClick(); 
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );
  }

  getWantToApply(labeledJobs){
    let want=[];
    for(let i=0;i<labeledJobs.length;i++){
      if(labeledJobs[i].label=="Want to Apply"){
        want.push(labeledJobs[i]);
      }
    }
    return want;

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
      if (!this.wantToApply[i]){
        break;
      }
      this.viewedQueries.push(this.wantToApply[i]);
    } 
  }

}
