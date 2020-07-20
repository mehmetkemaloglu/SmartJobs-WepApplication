import { Component, OnInit, Input } from '@angular/core';
import { FormControl, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../user.service';
import { Location } from '@angular/common';
import { takeUntil } from 'rxjs/operators';

import tooltipData from '../../assets/tooltipDescription.json';
import countryListData from '../../assets/countries.json';
import fieldListData from '../../assets/fields.json';
import jobTypeListData from '../../assets/jobType.json';

import { LoginService } from '../login.service';



@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  selectedKeyword;
  countryList;
  fieldList;
  jobTypeList;
  selectedCountry;
  selectedField;
  selectedJobType;
  tempUrl;
  keyword1;
  searchResults=[];
  loading;
  queryMessage="";
  tooltip;
  isQuickSearch=false;
  quickSearchButtons;
  element;
  //paging variables
  viewedJobs;
  currentPage=1;
  numOfItemsInPage=10;
  pageNum: number;
  nums=[];
  constructor(
    private userService: UserService,
    private loginService: LoginService,
    public fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router

    ) {
    this.tooltip=tooltipData.search;
    this.countryList=countryListData;
    this.fieldList=fieldListData;
    this.jobTypeList=jobTypeListData;
 
    //console.log(this.userService.currentSearchedJobList);
    this.searchResults=this.userService.currentSearchedJobList;
   }
   searchForm = this.fb.group({
    keyword: [''],
    country: [''],
    jobType: [''], 
    field: ['']
  })

  ngOnInit() {
    this.nums=[];
    this.currentPage=1;
    this.searchResults=this.userService.currentSearchedJobList;
    if(undefined !== this.searchResults){
      this.pageNum=Math.ceil(this.searchResults.length/this.numOfItemsInPage);
      for (let i = 1; i<=this.pageNum;i++){
        this.nums.push(i);
      }
      this.getviewedQueriesByPage();
    }
    this.getQuickSearchButtons();
    this.getQuickSearchResults2();
    this.getSearchResults();
  }


  getUrlValues(){
    this.keyword1 = this.route.snapshot.paramMap.get('keyword');
    if (this.keyword1==" "){
      this.keyword1=null;
    }

    const country1 = this.route.snapshot.paramMap.get('country');
    const field1 = this.route.snapshot.paramMap.get('field');
    const jobType1 = this.route.snapshot.paramMap.get('jobType');

    this.searchForm.controls['country'].setValue(country1, {onlySelf: true});
    this.searchForm.controls['jobType'].setValue(jobType1, {onlySelf: true});
    this.searchForm.controls['field'].setValue(field1, {onlySelf: true});

    this.searchForm.patchValue({keyword: this.keyword1});
    this.selectedCountry=country1;
  }

  onSubmit() {
    //console.log("neden girmiyosun?");
    this.nums=[];
    this.currentPage=1;
    this.viewedJobs=[];
    this.searchResults=[];
    this.selectedKeyword=this.searchForm.value.keyword;
    this.selectedCountry=this.searchForm.value.country;
    this.selectedField=this.searchForm.value.field;
    this.selectedJobType=this.searchForm.value.jobType;
    //const url=this.createUrlFromSearchForWebsite(this.selectedKeyword,this.selectedCountry,this.selectedField,this.selectedJobType);
    this.tempUrl=this.createUrlFromSearchForRequest(this.selectedKeyword,this.selectedCountry,this.selectedField,this.selectedJobType);
    this.loading="Loading...";
    this.userService.getSearchData(this.tempUrl);
  }

  getSearchResults(){
    this.userService.isSearchResultsReady.subscribe((isReady) =>{
      if(isReady) {
        this.queryMessage="";
        this.searchResults = this.userService.getSearchResults();
        this.userService.currentSearchedJobList=this.searchResults;
        this.loading="";
        console.log(this.searchResults);
        this.pageNum=Math.ceil(this.searchResults.length/this.numOfItemsInPage);
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        if(this.searchResults.length==0){
          this.loading="Not available"
        }
      }
    },
    err=>{
      console.log(err);
      this.loading="An error occured, please try again later";
    }
    );
  }

  getQuickSearchButtons(){
    this.userService.getQuickSearch()
      .subscribe(res=> {
        this.quickSearchButtons=res;
        for (let i = 0;i<this.quickSearchButtons.length;i++){
          if(this.quickSearchButtons[i].fields.length==2){
            this.quickSearchButtons[i].fields="";
          }
          else{
            this.quickSearchButtons[i].fields=this.quickSearchButtons[i].fields.substring(2,this.quickSearchButtons[i].fields.length-2)
          }
          if(this.quickSearchButtons[i].jobtypes.length==2){
            this.quickSearchButtons[i].jobtypes="";
          }
          else{
            this.quickSearchButtons[i].jobtypes=this.quickSearchButtons[i].jobtypes.substring(2,this.quickSearchButtons[i].jobtypes.length-2)
          }
        }
        
      },
      err=>{
        console.log(err);
      });
  }

  getQuickSearchResults(searchButton, $element){
    console.log($element);
    this.element=$element;
    this.nums=[];
    this.currentPage=1;
    this.viewedJobs=[];
    this.searchResults=[];
    let id_=searchButton.id;
    this.searchForm.value.keyword=searchButton.keyword;
    this.searchForm.value.country=searchButton.location;
    this.searchForm.value.field=searchButton.fields;
    this.searchForm.value.jobType=searchButton.jobtypes;
    this.userService.getQuickSearchData(id_);
  }

  getQuickSearchResults2(){
    this.userService.isQuickSearchResultsReady.subscribe((isReady) =>{
      if(isReady) {
        this.searchResults = this.userService.getQuickSearchResults();
        console.log(this.searchResults);
        //this.userService.currentSearchedJobList=this.searchResults;
        this.loading="";
        this.pageNum=Math.ceil(this.searchResults.length/this.numOfItemsInPage);
        this.nums=[];
        for (let i = 1; i<=this.pageNum;i++){
          this.nums.push(i);
        }
        this.getviewedQueriesByPage();
        if(this.searchResults.length==0){
          this.loading="Not available"
        }
        this.element.scrollIntoView({behavior: "smooth", block: "start", inline: "end"});
      }
    },
    err=>{
      console.log(err);
    }
    );
  }


  goToJobSite(job){
    if(this.isQuickSearch){
      this.router.navigate(['/job-page/'+job.jid]);
    }
    else{
      this.router.navigate(['/job-page/'+job.jid]);
      //window.open('/job-page/'+job.jid, '_blank');
    }

  }

  saveQuery(){
    this.selectedKeyword=this.searchForm.value.keyword;
    this.selectedCountry=this.searchForm.value.country;
    this.selectedField=this.searchForm.value.field;
    this.selectedJobType=this.searchForm.value.jobType;
    let body=this.createQueryBodyForRequest(this.selectedKeyword,this.selectedCountry,this.selectedField,this.selectedJobType);
    //console.log(body);
    this.queryMessage="Saving...";
    this.userService.saveQuery(body)
      .subscribe(res=>{
        this.queryMessage="The search query has been saved."
        },
        err=>{
          console.log(err);
          this.queryMessage=err.error.message;
        }
      );
  }

  likeJob(job){
    this.userService.likeJob(job)
      .subscribe(res=>{
        console.log(job.id+"liked");
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
    this.viewedJobs=[];
    for (let i = (this.currentPage-1)*this.numOfItemsInPage;i<(this.currentPage)*this.numOfItemsInPage;i++){
      if (!this.searchResults[i]){
        break;
      }
      this.viewedJobs.push(this.searchResults[i]);
    } 
  }

  changeSearchMethod(){
    this.searchResults=[];
    this.viewedJobs=[];
    this.nums=[];
    this.pageNum;
    this.isQuickSearch=!this.isQuickSearch;
  }

  isSearchResultAvailable(){
    if(this.searchResults.length==0){
      return false;
    }
    else{
      return true;
    }
  }

  isLoggedIn(){
    return this.loginService.loggedIn();
  }

  createQueryBodyForRequest(keyword,country,field,jobType){
    if (keyword==" ")
      keyword="";
    if (country==" " || country=="-Country-")
      country="";
    if (field==" " || field=="All Fields")
      field="";
    if (jobType==" " || jobType=="All Job Types")
      jobType="";
    var queryBody={
      "keyword":keyword,
      "locations":country,
      "jobTypes":field,
      "fields":jobType,
      "personid":this.userService.getUserID()
    }
    return queryBody;
  }


  createUrlFromSearchForRequest(keyword,country,field,jobType){
    if (keyword==" ")
      keyword="";
    if (country==" " || country=="-Country-")
      country="";
    if (field==" " || field=="All Fields")
      field="";
    if (jobType==" " || jobType=="All Job Types")
      jobType="";
    const url="api/ap/?keyword="+keyword+"&locations="+country+"&fields="+field+"&jobtypes="+jobType+"&allJobs=true";
    return url;
  }
  createUrlFromSearchForWebsite(keyword,country,field,jobType){
    if (!keyword)
      keyword=" ";
    if (!country)
      country=" ";
    if (!field)
      field=" ";
    if (!jobType)
      jobType=" ";
    const url="/search/keyword/"+keyword+"/location/"+country+"/field/"+field+"/jobType/"+jobType;
    return url;
  }

}
