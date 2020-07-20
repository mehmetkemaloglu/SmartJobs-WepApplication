import { Component, OnInit} from '@angular/core';
import { UserService } from '../user.service';
import { ActivatedRoute, Router } from '@angular/router';
import { LoginService } from '../login.service';
import tooltipData from '../../assets/tooltipDescription.json';
import { EventEmitterService } from '../event-emitter.service';

@Component({
  selector: 'app-job-page',
  templateUrl: './job-page.component.html',
  styleUrls: ['./job-page.component.scss']
})
export class JobPageComponent implements OnInit {
  jobData;
  loading1="";
  loading2="";
  labels=[]; 
  label="";
  isLiked=false;
  wantToApply=false;
  jid;
  fields;
  tooltip;
 
  constructor(
    private userService:UserService, 
    private route: ActivatedRoute, 
    private loginService: LoginService,
    private router: Router,
    private eventEmitterService: EventEmitterService
    ) {
    this.tooltip=tooltipData.jobPage;
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.jid = params.get('jid');
      console.log(this.jid);
      this.getJobById();
    });
    
  }

  getJobById(){
    this.loading1="Loading job details..."
    this.userService.getJobById(this.jid)
      .subscribe( res=>{
        this.jobData=res;
        if(this.loginService.loggedIn){
          this.isLiked=this.jobData.liked;
        }
        let tempFields=this.jobData.fields.substring(1,this.jobData.fields.length-1);
        let tempFields2="";
        for(let letter of tempFields){
          if(letter!=="\""){
            tempFields2+=letter;
          }
        }
        this.jobData.fields=tempFields2;
        this.loading1="";
        console.log(this.jobData);
        if(this.loginService.loggedIn()){
          this.getLabelsOfAJob();
        }
        },
        err=>{
          console.log(err);
          this.loading1="An error occured on loading job details, please try again later"
        }
      );
  }
  
  getLabelsOfAJob(){
    this.loading2="Loading labels..."
    this.userService.getLabelsOfAJob(this.jid)
      .subscribe( res=>{
        this.labels=res;
        for(let i=0;i<this.labels.length;i++){
          if(this.labels[i]=="Want to Apply"){
            this.wantToApply=true;
            this.labels.splice(i, 1);
            break;
          }
        }
        
        this.loading2="";
        
        },
        err=>{
          console.log(err);
          this.loading2="An error occured on loading labels, please try again later"
        }
      );
  }

  addLabel(){
    this.loading2="Adding label..."
    if (this.label && this.labels.indexOf(this.label)== -1){
      this.userService.addLabel(this.jobData,this.label)
      .subscribe( res=>{
        this.loading2="";
        this.labels.push(this.label);
        this.label=""; 
        },
        err=>{
          console.log(err);
          this.loading2="An error occured, please try again later"
        }
      );      
    }
    else{
      this.loading2="This label is available"
    }
  }

  deleteLabel(selectedLabel){
    const index = this.labels.indexOf(selectedLabel);
    if (index > -1) {
      this.loading2="Deleting..."
      this.userService.deleteLabelFromJob(selectedLabel,this.jobData.jid)
        .subscribe( res=>{
          this.labels.splice(index, 1);
          selectedLabel="";
          this.loading2="";
          },
          err=>{
            console.log(err);
            this.loading2="An error occured, please try again later"
          }
        );
    }
  }

  addWantToApply(){
    this.loading2="Adding Want to Apply..."
    if (this.labels.indexOf("Want to Apply")== -1){
      this.userService.addLabel(this.jobData,"Want to Apply")
      .subscribe( res=>{
        this.loading2="";
        this.wantToApply=!this.wantToApply;
        this.eventEmitterService.onFirstComponentButtonClick(); 
        },
        err=>{
          console.log(err);
          this.loading2="An error occured, please try again later"
        }
      );
    }
    else{
      this.loading2="This label is available"
    }
  }

  deleteWantToApply(){
    if (this.wantToApply) {
      this.loading2="Deleting Want to Apply..."
      this.userService.deleteLabelFromJob("Want to Apply",this.jobData.jid)
        .subscribe( res=>{
          this.loading2="";
          this.wantToApply=!this.wantToApply;
          this.eventEmitterService.onFirstComponentButtonClick(); 
          },
          err=>{
            console.log(err);
            this.loading2="An error occured, please try again later"
          }
        );
    }
  }

  likeJob(){
    this.loading2="Like...";
    this.userService.likeJob(this.jobData)
      .subscribe(res=>{
        console.log(this.jobData.jid+"liked");
        this.loading2=""
        this.isLiked=!this.isLiked;
        },
        err=>{
          console.log(err);
          this.loading2="An error occured during the like, please try again later"
        }
      );
  }

  removeLike(){
    this.loading2="Removing Like";
    this.userService.removeLike(this.jobData.jid)
    .subscribe(res=>{
      console.log(this.jobData.jid+" like deleted");
      this.loading2="";
      this.isLiked=!this.isLiked;
      },
      err=>{
        console.log(err);
        this.loading2="An error occured during removing the like, please try again later"
      }
    );
  }

  goToJobSite(){
    window.open(this.jobData.link, '_blank');
  }

  isLoggedIn(){
    return this.loginService.loggedIn();
  }

  isJobHtmlNull(){
    return this.jobData.jobhtml===undefined;
  }
}
