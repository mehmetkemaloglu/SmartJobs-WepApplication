import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, Router } from '@angular/router';

import tooltipData from '../../assets/tooltipDescription.json';

@Component({
  selector: 'app-labeled',
  templateUrl: './labeled.component.html',
  styleUrls: ['./labeled.component.scss']
})
export class LabeledComponent implements OnInit {
  labels;
  selectedLabel="";
  loading="";
  labeledJobs=[];
  allLabeledJobs=[];
  selectedLabels=[];
  likedJobs;
  tooltip;
  constructor(private userService: UserService,
    private router: Router) {
      this.tooltip=tooltipData.labeled
     }

  ngOnInit() {
    this.getLabels();
    this.getSavedJobs();
  }

  getSavedJobs(){
    //this.loading="Loading..."
    this.userService.getSavedJobs()
      .subscribe( res=>{
        this.labeledJobs=res;
        this.labeledJobs=this.returnNonRecurrentJobs();
        this.allLabeledJobs=res;
        console.log(this.labeledJobs);
        //this.loading="";
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );

  }
  
  getLabels(){
    this.loading="Loading labels..."
    this.userService.getLabels()
      .subscribe( res=>{
        this.labels=res;
        for (let i = 0; i<this.labels.length;i++){
          if(this.labels[i]==="Want to Apply"){
            this.labels.splice(i,1);
          }
        }
        this.selectedLabels=this.labels;
        this.loading="";
        
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );

  }

  selectLabel(label){
    let isAdded=false;
    this.labeledJobs=[];
    if(!this.selectedLabel){
      this.selectedLabels=[];
    }
    this.selectedLabel=label;
    let index_=this.selectedLabels.indexOf(label);
    if (index_>-1){
      this.selectedLabels.splice(index_, 1);
      console.log(this.selectedLabels);
      isAdded=false;
    }
    else{
      this.selectedLabels.push(label);
      isAdded=true;
    }
    for(let i=0;i<this.allLabeledJobs.length;i++){
      let isSelected=false;
      //for(let label_ of this.allLabeledJobs[i].label){  if there is only 1 label enhanced for loop divides the label to letters :/
      let label_="";
      
      if (this.allLabeledJobs[i].label[0].length==1){
        label_=this.allLabeledJobs[i].label
        
        if (this.selectedLabels.indexOf(label_) > -1){
          isSelected=true;
        } 
      }
      else{
        for(let j=0;j<this.allLabeledJobs[i].label.length;j++){ 
          label_=this.allLabeledJobs[i].label[j];
          if (this.selectedLabels.indexOf(label_) > -1){
            isSelected=true;
            //break;
          } 
        }
      }
      if (isSelected){
        this.labeledJobs.push( this.allLabeledJobs[i])
      }
    }
    this.labeledJobs=this.returnNonRecurrentJobs();
  }

  deleteLabel(){
    const index = this.labels.indexOf(this.selectedLabel, 0);
    if (index > -1) {
      this.loading="Deleting..."
      this.userService.deleteLabelFromAll(this.selectedLabel)
        .subscribe( res=>{
          this.labels.splice(index, 1);
          this.selectedLabel="";
          this.loading="";
          },
          err=>{
            console.log(err);
            this.loading="An error occured, please try again later"
          }
        );
    }
  }

  likeJob(job){
    this.userService.likeJob(job)
      .subscribe(res=>{
        console.log(job.jid+"liked");
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
      );
  }

  

  


  isSelected(label){
    return this.selectedLabels.indexOf(label) >-1;
  }
  goToJobSite(job){
    console.log(job.jid);
    this.userService.currentJob=job;
    this.router.navigate(['/job-page/'+job.jid]);
  }

  getNonRecurrentJobs(jobs){
    let nonRecurrentJobs=[];
    console.log(jobs.length);
    for(let i=0;i<jobs.length;i++){
      console.log(nonRecurrentJobs.indexOf(jobs[i]))
      if(nonRecurrentJobs.indexOf(jobs[i])==-1){
        nonRecurrentJobs.push(jobs[i]);
      }
    }
    return nonRecurrentJobs;

  }

  returnNonRecurrentJobs(){
    let nonRecurrentJobs=[];
    let availableJobIds=[];
    for(let i=0;i<this.labeledJobs.length;i++){
      let index_=availableJobIds.indexOf(this.labeledJobs[i].jid);
      if (index_==-1 && this.labeledJobs[i].label!=="Want to Apply"){
        availableJobIds.push(this.labeledJobs[i].jid);
        nonRecurrentJobs.push(this.labeledJobs[i]);
           
      }
    }
    return nonRecurrentJobs;
  }

}
