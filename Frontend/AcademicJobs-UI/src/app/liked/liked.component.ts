import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, Router } from '@angular/router';

import tooltipData from '../../assets/tooltipDescription.json';

@Component({
  selector: 'app-liked',
  templateUrl: './liked.component.html',
  styleUrls: ['./liked.component.scss']
})
export class LikedComponent implements OnInit {

  loading="";
  likedJobs;
  tooltip;
  //paging variables
  viewedQueries;
  currentPage=1;
  numOfItemsInPage=10;
  pageNum: number;
  nums=[];

  constructor(private userService: UserService,
    private router: Router ) {
      this.tooltip=tooltipData.liked;
     }

  ngOnInit() {
    this.getLikedJobs();
  }

  getLikedJobs(){
    this.loading="Loading..."
    this.userService.getLikedJobs()
      .subscribe( res=>{
        this.likedJobs=res;
        this.pageNum=Math.ceil(this.likedJobs.length/this.numOfItemsInPage);
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        this.loading="";

        if(!this.likedJobs){
          this.loading="Not available"
        }
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

  remove(id){
    this.loading="Deleting..."
    let id_= id+((this.currentPage-1)*this.numOfItemsInPage);
    this.userService.removeLike(this.likedJobs[id_].jid)
      .subscribe( res=>{
        this.likedJobs.splice(id_, 1);
        this.loading="";
        if (this.likedJobs.length%this.numOfItemsInPage==0){
          console.log("page deleted");
          this.nums.splice(this.nums.length-1,1);
        }
        if (this.likedJobs.length == id_  && id==0 && this.currentPage>1){
          console.log("page changed");
          this.currentPage--;
        }
        this.getviewedQueriesByPage();
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );
  }

  selectPage(i){
    this.currentPage=i;
    this.getviewedQueriesByPage();
  }

  getviewedQueriesByPage(){
    this.viewedQueries=[];
    for (let i = (this.currentPage-1)*this.numOfItemsInPage;i<(this.currentPage)*this.numOfItemsInPage;i++){
      if (!this.likedJobs[i]){
        break;
      }
      this.viewedQueries.push(this.likedJobs[i]);
    } 
  }

}
