import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';

import tooltipData from '../../assets/tooltipDescription.json';

@Component({
  selector: 'app-search-queries',
  templateUrl: './search-queries.component.html',
  styleUrls: ['./search-queries.component.scss']
})
export class SearchQueriesComponent implements OnInit {
  loading=""
  queryMessage="";
  editField: string;
  mockQueries=[];
  tooltip;
  fetch="Fetch Jobs by Saved Queries" ;
  fetchTooltip="Next fetch will start at 03:30";
  //paging
  viewedQueries;
  currentPage=1;
  numOfItemsInPage=10;
  pageNum: number;
  nums=[];
  constructor(private userService: UserService) {
    this.tooltip=tooltipData.searchQueries;
  }

  ngOnInit() {
    this.getSearchedQueries()
  }
  
  getSearchedQueries(){
    
    this.loading="Loading..."
    this.userService.getSearchedQueries()
      .subscribe( res=>{
        this.mockQueries=res;
        this.pageNum=Math.ceil(this.mockQueries.length/this.numOfItemsInPage);
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        this.loading="";
        console.log(this.mockQueries);
        if(this.mockQueries.length==0){
          this.loading="Not available"
        }
        },
        err=>{
          console.log(err);
          this.loading="An error occured, please try again later"
        }
    );
  }
  
  remove(id: any) {
    this.queryMessage="Deleting..."
    let id_= id+((this.currentPage-1)*this.numOfItemsInPage);
    this.userService.removeQuery(this.mockQueries[id_].id)
      .subscribe(res=>{
        this.queryMessage="The query has been deleted."
        this.mockQueries.splice(id_, 1);
        if (this.mockQueries.length%this.numOfItemsInPage==0){
          console.log("page deleted");
          this.nums.splice(this.nums.length-1,1);
        }
        if (this.mockQueries.length == id_  && id==0 && this.currentPage>1){
          console.log("page changed");
          this.currentPage--;
        }
        this.getviewedQueriesByPage();
        },
        err=>{
          console.log(err);
          this.queryMessage="An error occured, please try again later"
        }
    );
  }

  changeValue(id: number, property: string, event: any) {
    this.editField = event.target.textContent;
  }

  updateList(id: number, property: string, event: any) {
    
    const editField = event.target.textContent;
    let id_= id+((this.currentPage-1)*this.numOfItemsInPage);

    if (editField===this.mockQueries[id_].keyword){
      return 0;
    }

    let body=this.createQueryBodyForRequest(this.mockQueries[id_],editField);
    this.queryMessage="Updating..."
    
    this.userService.removeQuery(this.mockQueries[id_].id)
      .subscribe(res=>{
        this.userService.saveQuery(body)
          .subscribe(res=>{
            this.mockQueries[id_][property] = editField;
            this.getviewedQueriesByPage();
            this.queryMessage="The search query has been updated."
            },
            err=>{
              console.log(err);
              this.queryMessage="An error occured, the query is unintentioanally deleted."
              this.mockQueries.splice(id_, 1);
              this.getviewedQueriesByPage();
            }
          );
        },
        err=>{
          console.log(err);
          this.queryMessage="An error occured, please try again later"
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
      if (!this.mockQueries[i]){
        break;
      }
      this.viewedQueries.push(this.mockQueries[i]);
    } 
  }

  fetchQueries(){
    this.fetch="Fetching...";
    this.fetchTooltip="This may take a while";
    setTimeout(() => this.fetchQueries2(),10000*this.mockQueries.length+10000);
  }

  fetchQueries2(){
    this.fetch="Fetch Jobs by Saved Queries";
    let tempDate= new Date();
    let tempHour=tempDate.getHours().toString();
    let tempMin=tempDate.getMinutes().toString();
    if (tempHour.length==1){
      tempHour="0"+tempHour;
    }
    if (tempMin.length==1){
      tempMin="0"+tempMin;
    }
    this.fetchTooltip="Last fetched at "+tempHour+":"+tempMin+". Next fetch will start at 03:30";

  }

  createQueryBodyForRequest(query,keyword_){
    var queryBody={
      "keyword":keyword_,
      "locations":query.location,
      "jobTypes":query.fields[0],
      "fields":query.jobtypes[0],
      "personid":this.userService.getUserID()
      //"personid":"2"
    }
    return queryBody;
  }
}
