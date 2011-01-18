#include <iostream>

//using namespace boost::python;
//using namespace std;
//#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

#include "particuleC.cpp"
//#include "data.cpp"

/*  Numérotation des stat
 * 	1 : nal			-1 : nha			-13 : fst
 *  2 : het			-2 : nss            -14 : aml
 *  3 : MGW			-3 : mpd
 *  4 : var			-4 : vpd
 *  5 : Fst			-5 : dta
 *  6 : lik			-6 : pss
 *  7 : dm2			-7 : mns
 *  8 : n2P			-8 : vns
 *  9 : h2P			-9 : nh2
 * 10 : v2P		   -10 : ns2
 * 11 : das        -11 : mp2
 * 12 : Aml        -12 : mpb
 *
 *
 */

int getwordint(string s,int num){
	s.append(" ");
	while (s.find(" ")== 0) s=s.substr(1);
	int i=1,j;
	while ((i<num)and(s.length()>1)) {
		j=s.find(" ");
		s=s.substr(j);
		while (s.find(" ")== 0) s=s.substr(1);
		i++;
	}
	s=s.substr(0,s.find(" "));
	if ((s.find("(")==0)or(s.find("[")==0)) s=s.substr(1,s.length()-1);
	return atoi(s.c_str());
}

double getwordfloat(string s,int num){
	s.append(" ");
	while (s.find(" ")== 0) s=s.substr(1);
	int i=1,j;
	while ((i<num)and(s.length()>1)) {
		j=s.find(" ");
		s=s.substr(j);
		while (s.find(" ")== 0) s=s.substr(1);
		i++;
	}
	s=s.substr(0,s.find(" "));
	if ((s.find("(")==0)or(s.find("[")==0)) s=s.substr(1,s.length()-1);
	return atof(s.c_str());
}

string* splitwords(string s,string sep,int *k){
	int j=0,j0,j1;
	while (s.find(sep)== 0) s=s.substr(1);
	*k=0;
	s.append(sep);
	string *sb,s0,s1;
	s1=string();
	for (int i=0;i<s.length();i++) {
		s0=s.substr(i,1);
		if (s0==sep){
			j++;
			if (j==1) {
				s1.append(s0);
				if (j==1) (*k)++;
				cout <<" j=1  k="<<*k<<"\n";
			}
		} else {
			s1.append(s0);
			j=0;
		}
	}
	sb = new string[*k];
	for (int i=0;i<*k;i++) {
		j0=s1.find(sep);
		sb[i]=s1.substr(0,j0);
		s1=s1.substr(j0+1,s.length());

	}
	cout <<"k="<<*k<<"\n";
	return sb;
}

int ndecimales(double pp){
  double p;
  int k;
  p = pp;
  k = 0;
  while (abs(p-round(p))>1E-15) {k++;p=10*p;}
  return k;
}


class Scenario
{
public:
	double *parameters,prior_proba;
    int number,popmax,npop,nsamp,*time_sample,nparam,nevent,nn0;
    EventC *event;
    Ne0C *ne0;
    HistParameterC *histparam;
    /* action = 0 (varne), 1 (merge), 2 (split), 3 (adsamp)
     * category=0 (Ne)   , 1 (time),  3 (admixrate)
    */

    void read_events(int nl,string *ls){
    	string *ss;
    	int n;
    	ss = splitwords(ls[0]," ",&n);
    	this->nn0=n;
    	this->ne0 = new Ne0C[this->nn0];
    	for (int i=0;i<this->nn0;i++) {
    		if (atoi(ss[i].c_str())!=0) {this->ne0[i].name=n0[i];this->ne0[i].val=-1;}
    		else               {this->ne0[i].name="";this->ne0[i].val=atoi(ss[i]);}
    	}
    	this->event = new EventC[nl-1];
    	for (int i=0;i<nl-1;i++) {
    		ss = splitwords(ls[i+1]," ",&n);
    		this->event[i].stime="";this->event[i].sNe="";this->event[i].sadmixrate="";
    		if (ss[0]=="0") {this->event[i].time=0;}
    		else if (atoi(ss[0].c_str())==0) {this->event[i].time=0;this->event[i].stime=ss[0];}
    			 else {this->event[i].time=atoi(ss[0].c_str());}
    		if (majuscules(ss[1])=="SAMPLE") {
    			this->event[i].action=3;
    			this->event[i].pop=atoi(ss[2].c_str());
    		} else if (majuscules(ss[1])=="MERGE") {
    			this->event[i].pop=atoi(ss[2].c_str());
    			this->event[i].pop1=atoi(ss[3].c_str());
    		} else if (majuscules(ss[1])=="SPLIT") {
    			this->event[i].pop=atoi(ss[2].c_str());
    			this->event[i].pop1=atoi(ss[3].c_str());
    			this->event[i].pop2=atoi(ss[4].c_str());
    			if (atof(ss[5].c_str())!=0.0) this->event[i].admixrate=atof(ss[5].c_str());
    			else {this->event[i].admixrate=0.0;this->event[i].sadmixrate=ss[5];}
    		} else if (majuscules(ss[1])=="VARNE") {
    			this->event[i].pop=atoi(ss[2].c_str());
    			if (atof(ss[3].c_str())!=0.0) this->event[i].Ne=atoi(ss[3].c_str());
    			else {this->event[i].Ne=0;this->event[i].sNe=ss[3];}
    		}
    	}
    }
};

PriorC copyprior(PriorC source) {
	PriorC dest;
	dest.loi = source.loi;
	dest.mini = source.mini;
	dest.maxi = source.maxi;
	dest.mean = source.mean;
	dest.sdshape = source.sdshape;
	dest.constant = source.constant;
	dest.ndec  = source.ndec;
	return dest;
}

class Header
{
public:
	string message,datafilename;
	DataC dataobs;
	int nparamtot,nstat,nscenarios,nconditions,ngroupes;
	Scenario *scenario;
	HistParameterC *histparam;
	ConditionC *condition;
	LocusGroupC *groupe;

	PriorC readprior(string ss) {
		double step;
		PriorC prior;
		string s1,*sb;
		int j;
		s1 = ss.substr(3,ss.length()-4);
		sb = splitwords(s1,",",&j);
		step=atof(sb[4].c_str());
		prior.ndec=ndecimales(step);
		prior.mini=atof(sb[0].c_str());
		prior.maxi=atof(sb[1].c_str());
		if (ss.find("UN[")!=string::npos) {prior.loi="uniforme";}
		else if (ss.find("LU[")!=string::npos) {prior.loi="loguniforme";}
		else if (ss.find("NO[")!=string::npos) {prior.loi="normale";prior.mean=atof(sb[2].c_str());prior.sdshape=atof(sb[3].c_str());}
		else if (ss.find("LN[")!=string::npos) {prior.loi="lognormale";prior.mean=atof(sb[2].c_str());prior.sdshape=atof(sb[3].c_str());}
		else if (ss.find("GA[")!=string::npos) {prior.loi="gamma";prior.mean=atof(sb[2].c_str());prior.sdshape=atof(sb[3].c_str());}
		prior.constant = ((prior.maxi-prior.mini)/prior.maxi<0.000001);
		return prior;
	}

	ConditionC readcondition(string ss){
		ConditionC cond;
		if (ss.find(">=")!=string::npos){
			cond.operateur=">=";cond.param1=ss.substr(0,ss.find(">="));cond.param2=ss.substr(ss.find(">=")+2,ss.length()-(ss.find(">=")+2));}
		else if (ss.find("<=")!=string::npos){
			cond.operateur="<=";cond.param1=ss.substr(0,ss.find("<="));cond.param2=ss.substr(ss.find("<=")+2,ss.length()-(ss.find("<=")+2));}
		if (ss.find(">")!=string::npos){
			cond.operateur=">";cond.param1=ss.substr(0,ss.find(">"));cond.param2=ss.substr(ss.find(">")+1,ss.length()-(ss.find(">")+1));}
		else if (ss.find("<=")!=string::npos){
			cond.operateur="<";cond.param1=ss.substr(0,ss.find("<"));cond.param2=ss.substr(ss.find("<")+1,ss.length()-(ss.find("<")+1));}
	}

	void assignloc(int gr){
		this->groupe[gr].nloc = 0;
		for (int loc=0;loc<dataobs.nloc;loc++) {
			if (dataobs.locus[loc].groupe==gr+1) this->groupe[gr].nloc++;
		}
		this->groupe[gr].loc = new int[this->groupe[gr].nloc];
		int iloc=-1;
		for (int i=0;i<dataobsi;loc++) {
			if (dataobs.locus[i].groupe==gr+1) {iloc++;this->groupe[gr].loc[iloc] = i;}
		}
	}

	void readHeader(){
		string s1,**sl,*ss,*ss1;
		int *nlscen,nss,nss1,j,k,l,gr,grm;
		ifstream file("ReftableHeader.txt", ios::in);
		if (file == NULL) {
			this->message = "File ReftableHeader.txt not found";
			return this;
		} else this->message="";
		getline(file,this->datafilename);
		dataobs.loadfromfile(this->datafilename);
		getline(file,s1);
		this->nparamtot=getwordint(s1,1);
		this->nstat=getwordint(s1,4);
//Partie Scenarios
		getline(file,s1);		//ligne vide
		getline(file,s1);       // nombre de scenarios
		this->nscenarios=getwordint(s1,1);
		sl = new string*[this->nscenarios];
		nlscen = new int[this->nscenarios];
		scenario = new Scenario[this->nscenarios];
		for (int i=0;i<this->nscenarios;i++) nlscen[i]=getwordint(s1,3+i);
		for (int i=0;i<this->nscenarios;i++) {
			sl[i] = new string[nlscen[i]];
			getline(file,s1);
			scenario[i].number = getwordint(s1,2);
			scenario[i].prior_proba = getwordint(s1,3);
			scenario[i].nparam = getwordint(s1,4);
			for (int j=0;j<nlscen[i];j++) getline(file,sl[i][j]);
			scenario[i].read_events(nlscen[i],sl[i]);
		}
		for (int i=0;i<this->nscenarios;i++) delete []sl[i];
		delete [] sl;
//Partie historical parameters
		getline(file,s1);		//ligne vide
		getline(file,s1);
		ss=splitwords(s1," ",&nss);
		this->nparamtot = atoi(ss[3].c_str());
		if (nss>4) this->nconditions =  atoi(ss[4].c_str()); else  this->nconditions = 0;
		this->histparam = new PriorC[this->nparamtot];
		if (this->nconditions>0) this->condition = new prior[this->nconditions];
		delete [] ss;
		for (int i=0;i<this->nparamtot;i++) {
			getline(file,s1);
			ss=splitwords(s1," ",&nss);
			this->histparam[i].name=ss[0];
			if (ss[1]=="N") this->histparam[i].category = 0;
			else if  (ss[1]=="T") this->histparam[i].category = 1;
			else if  (ss[1]=="A") this->histparam[i].category = 2;
			this->histparam[i].prior = this->readprior(ss[2]);
		}
		delete [] ss;
		if (this->nconditions>0) {
			this->condition = new prior[this->nconditions];
			for (int i=0;i<this->nconditions;i++) {
				getline(file,s1);
				this->condition[i] = this->readcondition(s1);
			}
		}
//Partie loci description
		getline(file,s1);		//ligne vide
		getline(file,s1);		//ligne "loci description"
		grm=1;
		for (int loc=0;loc<dataobs.nloc;loc++){
			getline(file,s1);
			ss=splitwords(s1," ",&nss);
			k=0;while (ss[k].find("[")==string::npos) k++;
			if (ss[k]=="[M]") {
				s1=ss[k+1].substr(1,ss[k+1].length());gr=atoi(s1.c_str());dataobs.locus[loc].groupe=gr;if (gr>grm) grm=gr;
				dataobs.locus[loc].motif_size=atoi(ss[k+2].c_str());dataobs.locus[loc].motif_range=atoi(ss[k+3].c_str());
			}
			else if (ss[k]=="[S]") {
				s1=ss[k+1].substr(1,ss[k+1].length());gr=atoi(s1.c_str());dataobs.locus[loc].groupe=gr;if (gr>grm) grm=gr;
				dataobs.locus[loc].dnalength=atoi(ss[k+2].c_str());
			}
		}
		this->ngroupes=grm;
		delete [] ss;
//Partie group priors
		getline(file,s1);		//ligne vide
		getline(file,s1);		//ligne "group prior"
		this->groupe = new LocusGroupC[grm];
		for (gr=0;gr<grm;gr++){
			getline(file,s1);
			ss=splitwords(s1," ",&nss);
			this->assignloc(gr);
			if (ss[2]=="[M]") {this->groupe[gr].type=0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priormutmoy = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priormutmoy.constant) this->groupe[gr].mutmoy=this->groupe[gr].priormutmoy.mini; else this->groupe[gr].mutmoy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priormutloc = this->readprior(ss1[1]);delete [] ss1;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priorPmoy   = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priorPmoy.constant) this->groupe[gr].Pmoy=this->groupe[gr].priorPmoy.mini; else this->groupe[gr].Pmoy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priorPloc   = this->readprior(ss1[1]);delete [] ss1;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priorsnimoy = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priorsnimoy.constant) this->groupe[gr].snimoy=this->groupe[gr].priorsnimoy.mini; else this->groupe[gr].snimoy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priorsniloc = this->readprior(ss1[1]);delete [] ss1;
			} else if (ss[2]=="[S]") {this->groupe[gr].type=1;
				this->groupe[gr].p_fixe = atof(ss[3].c_str());
				this->groupe[gr].gams = atof(ss[4].c_str());
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priormusmoy = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priormusmoy.constant) this->groupe[gr].musmoy=this->groupe[gr].priormusmoy.mini; else this->groupe[gr].musmoy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priormusloc = this->readprior(ss1[1]);delete [] ss1;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priork1moy  = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priork1.constant) this->groupe[gr].k1moy=this->groupe[gr].priork1moy.mini; else this->groupe[gr].k1moy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priork1loc  = this->readprior(ss1[1]);delete [] ss1;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priork2moy  = this->readprior(ss1[1]);delete [] ss1;
				if (this->groupe[gr].priork2.constant) this->groupe[gr].k2moy=this->groupe[gr].priork2moy.mini; else this->groupe[gr].k2moy=-1.0;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);this->groupe[gr].priork2loc  = this->readprior(ss1[1]);delete [] ss1;
				getline(file,s1);ss1=splitwords(s1," ",&nss1);
				this->groupe[gr].p_fixe=atof(ss1[2].c_str());this->groupe[gr].gams=atof(ss1[3].c_str());
				if (ss1[0]=="JK") this->groupe[gr].mutmod=0;
				else if (ss1[0]=="K2P") this->groupe[gr].mutmod=1;
				else if (ss1[0]=="HKY") this->groupe[gr].mutmod=2;
				else if (ss1[0]=="TN") this->groupe[gr].mutmod=3;
			}
		}
		delete [] ss;
//Partie group statistics
		getline(file,s1);		//ligne vide
		getline(file,s1);		//ligne "group group statistics"
		for (gr=0;gr<grm;gr++) {
			getline(file,s1);
			ss=splitwords(s1," ",&nss);
			this->groupe[gr].nstat = atoi(ss[3]);
			this->groupe[gr].sumstat = new StatC[this->groupe[gr].nstat];
			delete [] ss;
			k=0;
			while (k<this->groupe[gr].nstat) {
				getline(file,s1);
				ss=splitwords(s1," ",&nss);
				j=0;while (ss[0]!=stat_type[j]) j++;
				this->groupe[gr].sumstat[k].cat=stat_num[j];
				if (this->groupe[gr].type==0) {
					if (stat_num[j]<5) {
						for (int i=1;i<nss;i++) {this->groupe[gr].sumstat[k].samp=atoi(ss[i].c_str());k++;}
					} else if (stat_num[j]<12) {
						for (int i=1;i<nss;i++) {
							ss1=splitwords(ss[i],"&",&nss1);
							this->groupe[gr].sumstat[k].samp=atoi(ss1[0].c_str());
							this->groupe[gr].sumstat[k].samp1=atoi(ss1[1].c_str());
							k++;
						}
						delete [] ss1;
					} else if (stat_num[j]==12) {
						for (int i=1;i<nss;i++) {
							ss1=splitwords(ss[i],"&",&nss1);
							this->groupe[gr].sumstat[k].samp=atoi(ss1[0].c_str());
							this->groupe[gr].sumstat[k].samp1=atoi(ss1[1].c_str());
							k++;
						}
					}
					delete [] ss1;
				} else if (this->groupe[gr].type==1) {
					if (stat_num[j]>-5) {
						for (int i=1;i<nss;i++) {this->groupe[gr].sumstat[k].samp=atoi(ss[i].c_str());k++;}
					} else if (stat_num[j]>-14) {
						for (int i=1;i<nss;i++) {
							ss1=splitwords(ss[i],"&",&nss1);
							this->groupe[gr].sumstat[k].samp=atoi(ss1[0].c_str());
							this->groupe[gr].sumstat[k].samp1=atoi(ss1[1].c_str());
							k++;
						}
						delete [] ss1;
					} else if (stat_num[j]==-14) {
						for (int i=1;i<nss;i++) {
							ss1=splitwords(ss[i],"&",&nss1);
							this->groupe[gr].sumstat[k].samp=atoi(ss1[0].c_str());
							this->groupe[gr].sumstat[k].samp1=atoi(ss1[1].c_str());
							this->groupe[gr].sumstat[k].samp2=atoi(ss1[2].c_str());
							k++;
						}
					}
					delete [] ss1;
				}
			}
			delete [] ss;
		}
//Entete du fichier reftable
		getline(file,s1);		//ligne vide
		getline(file,this->entete);		//ligne entete

	}
};

struct ParticleSetC
{
	ParticleC *particule;
	LocusC *locuslist;
	LocusGroupC *grouplist;
	int npart,nloc,ngr;
	int nsample,*nind,**indivsexe;
	double sexratio;

	void setdata(int p) {
		this->particule[p].data.nsample = dataobs.nsample;
		this->particule[p].data.nind = new int[dataobs.nsample];
		this->particule[p].data.indivsexe = new int*[dataobs.nsample];
		for (int i=0;i<dataobs.nsample;i++) {
			this->particule[p].data.nind[i] = dataobs.nind[i];
			this->particule[p].data.indivsexe[i] = new int[dataobs.nind[i]];
			for (int j=0;j<data.nind[i];j++) this->particule[p].data.indivsexe[i][j] = dataobs.indivsexe[i][j];
		}
	}

	void setgroup(int p) {
		int ngr = header.ngroupes;
		this->particule[p].ngr = ngr;
		this->particule[p].grouplist = new LocusGroupC[ngr];
		for (int gr=0;gr<this->ngr;gr++) {
			this->particule[p].grouplist[gr].type =header.groupe[gr].type;
			this->particule[p].grouplist[gr].nloc = header.groupe[gr].nloc;
			this->particule[p].grouplist[gr].loc  = new int[header.groupe[gr].nloc];
			for (int i=0;i<header.groupe[gr].nloc;i++) this->particule[p].grouplist[gr].loc[i] = header.groupe[gr].loc[i];
			if (header.groupe[gr].type==0) {	//MICROSAT
				this->particule[p].grouplist[gr].mutmoy = header.groupe[gr].mutmoy;
				if (header.groupe[gr].mutmoy<0.0) this->particule[p].grouplist[gr].priormutmoy = copyprior(header.groupe[gr].priormutmoy);
				else this->particule[p].grouplist[gr].priormutmoy.constant=true;
				this->particule[p].grouplist[gr].priormutloc = copyprior(header.groupe[gr].priormutloc);
				this->particule[p].grouplist[gr].Pmoy = header.groupe[gr].Pmoy;
				if (header.groupe[gr].Pmoy<0.0) this->particule[p].grouplist[gr].priorPmoy = copyprior(header.groupe[gr].priorPmoy);
				else this->particule[p].grouplist[gr].priorPmoy.constant=true;
				this->particule[p].grouplist[gr].priorPloc = copyprior(header.groupe[gr].priorPloc);
				this->particule[p].grouplist[gr].snimoy = header.groupe[gr].snimoy;
				if (header.groupe[gr].snimoy<0.0) this->particule[p].grouplist[gr].priorsnimoy = copyprior(header.groupe[gr].priorsnimoy);
				else this->particule[p].grouplist[gr].priorsnimoy.constant=true;
				this->particule[p].grouplist[gr].priorsniloc = copyprior(header.groupe[gr].priorsniloc);
			}
			else {							//SEQUENCES
				this->particule[p].grouplist[gr].mutmod = header.groupe[gr].mutmod;	//mutmod
				this->particule[p].grouplist[gr].p_fixe = header.groupe[gr].p_fixe;	//p_fixe
				this->particule[p].grouplist[gr].gams   = header.groupe[gr].gams;	//gams
				this->particule[p].grouplist[gr].musmoy = header.groupe[gr].musmoy;	//musmoy
				if (header.groupe[gr].musmoy<0.0) this->particule[p].grouplist[gr].priormusmoy = copyprior(header.groupe[gr].priormusmoy);
				else this->particule[p].grouplist[gr].priormusmoy.constant=true;
				this->particule[p].grouplist[gr].priormusloc = copyprior(header.groupe[gr].priormusloc);
				if (header.groupe[gr].mutmod>0){
					this->particule[p].grouplist[gr].k1moy = header.groupe[gr].k1moy ;	//k1moy
					if (header.groupe[gr].k1moy<0) this->particule[p].grouplist[gr].priork1moy = copyprior(header.groupe[gr].priork1moy);
					else this->particule[p].grouplist[gr].priork1moy.constant=true;
					this->particule[p].grouplist[gr].priork1loc = copyprior(header.groupe[gr].priork1loc);
				}
				if (header.groupe[gr].mutmod>2){
					this->particule[p].grouplist[gr].k2moy = header.groupe[gr].k2moy ;	//k2moy
					if (header.groupe[gr].k2moy<0) this->particule[p].grouplist[gr].priork2moy = copyprior(header.groupe[gr].priork2moy);
					else this->particule[p].grouplist[gr].priork2moy.constant=true;
					this->particule[p].grouplist[gr].priork2loc = copyprior(header.groupe[gr].priork2loc);
				}
			}
			this->particule[p].grouplist[gr].nstat=header.groupe[gr].nstat;
			this->particule[p].grouplist[gr].stat = new StatC[header.groupe[gr].nstat];
			for (int i=0;i<header.groupe[gr].nstat;i++){
				this->particule[p].grouplist[gr].stat[i].cat   = header.groupe[gr].stat[i].cat;
				this->particule[p].grouplist[gr].stat[i].samp  = header.groupe[gr].stat[i].samp;
				this->particule[p].grouplist[gr].stat[i].samp1 = header.groupe[gr].stat[i].samp1;
				this->particule[p].grouplist[gr].stat[i].samp2 = header.groupe[gr].stat[i].samp2;

			}
		}
	}

	void setloci(vector <int>loc_i, vector <double>loc_j) {
		int nloc;
		nloc = loc_i[0];
		this->nloc=nloc;
		this->locuslist = new LocusC[nloc];
		//for (int i=0;i<loc_j.size();i++) cout <<loc_j[i]<<"  ";cout<<"\n\n";
		//cout << nloc << " loci à transférer"<<"\n";
		int n = 0,m=-1;
		for (int kloc=0;kloc<nloc;kloc++){
			n +=1;this->locuslist[kloc].groupe =loc_i[n];
			n +=1;this->locuslist[kloc].type =loc_i[n];
			if (this->locuslist[kloc].type < 5) {
				n +=1;this->locuslist[kloc].kmin = loc_i[n];
				n +=1;this->locuslist[kloc].kmax = loc_i[n];
				n +=1;this->locuslist[kloc].motif_size = loc_i[n];
				n +=1;this->locuslist[kloc].motif_range = loc_i[n];
				m +=1;this->locuslist[kloc].mut_rate = loc_j[m];
				//cout << "mut_rate=" <<this->locuslist[kloc].mut_rate<<" (m="<<m<<")";
				if (this->locuslist[kloc].mut_rate<0.0) {
					this->locuslist[kloc].priormut.loi="GA";
					m++;this->locuslist[kloc].priormut.mini=loc_j[m];
					//cout << "  mini=" <<this->locuslist[kloc].priormut.mini<<" (m="<<m<<")";
					m++;this->locuslist[kloc].priormut.maxi=loc_j[m];
					//cout << "  maxi=" <<this->locuslist[kloc].priormut.maxi<<" (m="<<m<<")";
					m++;this->locuslist[kloc].priormut.sdshape=loc_j[m];
					//cout << "  sdshape=" <<this->locuslist[kloc].priormut.sdshape <<" (m="<<m<<")"<<"\n";
				}
				m +=1;this->locuslist[kloc].Pgeom = loc_j[m];
				//cout <<"\nPgeom = "<<this->locuslist[kloc].Pgeom<<"  (m="<<m<<")";
				if (this->locuslist[kloc].Pgeom<0.0) {
					this->locuslist[kloc].priorP.loi="GA";
					m++;this->locuslist[kloc].priorP.mini=loc_j[m];
					//cout << "  mini=" <<this->locuslist[kloc].priorP.mini;
					m++;this->locuslist[kloc].priorP.maxi=loc_j[m];
					//cout << "  maxi=" <<this->locuslist[kloc].priorP.maxi;
					m++;this->locuslist[kloc].priorP.sdshape=loc_j[m];
					//cout << "  sdshape=" <<this->locuslist[kloc].priorP.sdshape <<"\n";
				}
				m +=1;this->locuslist[kloc].sni_rate = loc_j[m];
				//cout <<"\nsni_rate = "<<this->locuslist[kloc].sni_rate<<"  (m="<<m<<")";
				if (this->locuslist[kloc].sni_rate<0.0) {
					this->locuslist[kloc].priorsni.loi="GA";
					m++;this->locuslist[kloc].priorsni.mini=loc_j[m];
					//cout << "  mini=" <<this->locuslist[kloc].priorsni.mini;
					m++;this->locuslist[kloc].priorsni.maxi=loc_j[m];
					//cout << "  maxi=" <<this->locuslist[kloc].priorsni.maxi;
					m++;this->locuslist[kloc].priorsni.sdshape=loc_j[m];
					//cout << "  sdshape=" <<this->locuslist[kloc].priorsni.sdshape <<"\n";
				}
//cout <<"\nlocus "<< kloc <<"  groupe "<< this->locuslist[kloc].groupe <<"  " <<this->locuslist[kloc].type<<","<< this->locuslist[kloc].kmin<<","<<this->locuslist[kloc].kmax<<","
//		<<this->locuslist[kloc].motif_size<<","<<this->locuslist[kloc].motif_range<<","<<this->locuslist[kloc].mut_rate<<","<<this->locuslist[kloc].Pgeom<<","
//		<<this->locuslist[kloc].sni_rate<<"\n";
				}
			else {
				n +=1;this->locuslist[kloc].dnalength = loc_i[n];
				m +=1;this->locuslist[kloc].mus_rate = loc_j[m];
				m +=1;this->locuslist[kloc].k1 = loc_j[m];
				m +=1;this->locuslist[kloc].k2 = loc_j[m];
				m +=1;this->locuslist[kloc].pi_A = loc_j[m];
				m +=1;this->locuslist[kloc].pi_C = loc_j[m];
				m +=1;this->locuslist[kloc].pi_G = loc_j[m];
				m +=1;this->locuslist[kloc].pi_T = loc_j[m];
				this->locuslist[kloc].mutsit = new double[this->locuslist[kloc].dnalength];
				for (int i=0;i<this->locuslist[kloc].dnalength;i++) {
					m +=1;this->locuslist[kloc].mutsit[i] = loc_j[m];
					//std::cout << this->locuslist[kloc].mutsit[i]<< "   ";
					}
				//std::cout <<"\n";
				}
			double coeff=0.0;
			//cout << "sex-ratio = " << this->sexratio << "\n";
			switch (this->locuslist[kloc].type % 5)
			{	case 0 :  coeff = 16.0range_siz*this->sexratio*(1.0-this->sexratio);break;
				case 1 :  coeff = 2.0;break;
				case 2 :  coeff = 18.0*this->sexratio*(1.0-this->sexratio)/(1.0+this->sexratio);break;
				case 3 :  coeff = 2.0*this->sexratio;break;
				case 4 :  coeff = 2.0*(1.0-this->sexratio);break;
			}
			this->locuslist[kloc].coeff=coeff;
			//cout << "locus " << kloc << "   type=" << this->locuslist[kloc].type << "   coeff=" << this->locuslist[kloc].coeff << "\n";
		}
		for (int p=0;p<this->npart;p++) {
			this->particule[p].nloc = nloc;
			this->particule[p].locuslist = new LocusC[nloc];
			for (int kloc=0;kloc<nloc;kloc++){
				this->particule[p].locuslist[kloc].type = this->locuslist[kloc].type;
				this->particule[p].locuslist[kloc].groupe = this->locuslist[kloc].groupe;
				if (this->locuslist[kloc].type < 5) {
					this->particule[p].locuslist[kloc].kmin = this->locuslist[kloc].kmin;
					this->particule[p].locuslist[kloc].kmax = this->locuslist[kloc].kmax;
					this->particule[p].locuslist[kloc].motif_size = this->locuslist[kloc].motif_size;
					this->particule[p].locuslist[kloc].motif_range = this->locuslist[kloc].motif_range;
					this->particule[p].locuslist[kloc].mut_rate = this->locuslist[kloc].mut_rate;
					if (this->locuslist[kloc].mut_rate<0.0) this->particule[p].locuslist[kloc].priormut = this->copyprior(this->locuslist[kloc].priormut);
					this->particule[p].locuslist[kloc].Pgeom = this->locuslist[kloc].Pgeom;
					if (this->locuslist[kloc].Pgeom<0.0) this->particule[p].locuslist[kloc].priorP = this->copyprior(this->locuslist[kloc].priorP);
					this->particule[p].locuslist[kloc].sni_rate = this->locuslist[kloc].sni_rate;
					if (this->locuslist[kloc].sni_rate<0.0) this->particule[p].locuslist[kloc].priorsni = this->copyprior(this->locuslist[kloc].priorsni);
					}
				else {
					this->particule[p].locuslist[kloc].dnalength = this->locuslist[kloc].dnalength;
					this->particule[p].locuslist[kloc].mus_rate = this->locuslist[kloc].mus_rate;
					this->particule[p].locuslist[kloc].k1 = this->locuslist[kloc].k1;
					this->particule[p].locuslist[kloc].k2 = this->locuslist[kloc].k2;
					this->particule[p].locuslist[kloc].pi_A =this->locuslist[kloc].pi_A ;
					this->particule[p].locuslist[kloc].pi_C = this->locuslist[kloc].pi_C;
					this->particule[p].locuslist[kloc].pi_G = this->locuslist[kloc].pi_G;
					this->particule[p].locuslist[kloc].pi_T = this->locuslist[kloc].pi_T;
					this->particule[p].locuslist[kloc].mutsit = new double[this->locuslist[kloc].dnalength];
					for (int i=0;i<locuslist[kloc].dnalength;i++) this->particule[p].locuslist[kloc].mutsit[i] = this->locuslist[kloc].mutsit[i];
					//std::cout <<"\n";
					}
				this->particule[p].locuslist[kloc].coeff = this->locuslist[kloc].coeff;
			}
		}
	}

		int calsamplesize(int loc,int samp) {
	    	int nn,ng=0;
			for (int ind=0;ind<this->nind[samp];ind++) {
				if ((this->locuslist[loc].type == 0)or((this->locuslist[loc].type == 2)and(this->indivsexe[samp][ind] == 2))) {nn=2;}
				else if ((this->locuslist[loc].type == 3)and(this->indivsexe[samp][ind] == 2)) {nn=0;}
				else {nn=1;}
				ng +=nn;
			}
//			cout << "ng=" <<ng << "\n";
			return ng;
	    }

	void setdataloc(vector<int> da, verange_sizctor<int> gri, vector<double> grd, vector<string> grs, vector<int> loci, vector<double>locj){
		setdata(da);
		setgroup(gri,grd,grs);
		setloci(loci,locj);
		int **ss;
		ss      = new int* [this->nloc];
		for (int loc=0;loc<this->nloc;loc++) {
			ss[loc] = new int [this->nsample];
			for (int samp=0;samp<this->nsample;samp++) {
				ss[loc][samp]=calsamplesize(loc,samp);
			}
		}
		for (int p=0;p<this->npart;p++) {
			for (int loc=0;loc<this->nloc;loc++) {
				this->particule[p].locuslist[loc].ss = new int[this->nsample];
				for (int sa=0;sa<this->nsample;sa++) this->particule[p].locuslist[loc].ss[sa] = ss[loc][sa];
			}
		}
		for (int loc=0;loc<this->nloc;loc++) delete []ss[loc];
		delete []ss;
	}

	void setevents (vector<int> eventi, vector<double> eventd, vector<string> events) {
		//cout << "debut de setevents\n";
		int nevent,popmax,*time_sample;
		EventC *eventlist;

		nevent = eventi[0];
		//cout << "nevent = "<<nevent<<"\n";
		eventlist = new EventC[nevent];
		time_sample = new int[this->nsample];
		int ni = 0, nd=-1, ns=-1,nsa=0;
		popmax=0;
		for (int kloc=0;kloc<nevent;kloc++){
			ni +=1;eventlist[kloc].time = eventi[ni];
			//cout << "time=" << eventlist[kloc].time;
			if (eventlist[kloc].time<0) {ns +=1;eventlist[kloc].stime = events[ns];}
			ni +=1;eventlist[kloc].action = eventi[ni];
			//cout <<"   action=" <<eventlist[kloc].action;
			ni +=1;eventlist[kloc].pop = eventi[ni];
			//cout <<"   pop="<<eventlist[kloc].pop;
			ni +=1;eventlist[kloc].pop1 = eventi[ni];
			//cout <<"   pop1="<<eventlist[kloc].pop1;
			ni +=1;eventlist[kloc].pop2 = eventi[ni];
			//cout <<"   pop2="<<eventlist[kloc].pop2;
			ni +=1;eventlist[kloc].sample =eventi[ni];
			//cout <<"   sample="<<eventlist[kloc].sample;
			ni +=1;eventlist[kloc].Ne = eventi[ni];
			//cout <<"   Ne="<<eventlist[kloc].Ne;
			if (eventlist[kloc].Ne<0) {ns +=1;eventlist[kloc].sNe =events[ns];}
			nd +=1;eventlist[kloc].admixrate =eventd[nd];
			//cout <<"   admixrate="<<eventlist[kloc].admixrate;
			if ((eventlist[kloc].admixrate<0)and(eventlist[kloc].action==3)) {ns +=1;eventlist[kloc].sadmixrate = events[ns];}
			ni +=1;eventlist[kloc].numevent0 =eventi[ni];
			//cout <<"   numevent0="<<eventlist[kloc].numevent0<<"\n";
			if (eventlist[kloc].action == 0) {
				time_sample[nsa] = eventlist[kloc].time;nsa +=1;
				}
			if (eventlist[kloc].pop>popmax){popmax=eventlist[kloc].pop;}
			}
		for (int p=0;p<this->npart;p++) {
			this->particule[p].nevent = nevent;
			this->particule[p].popmax = popmax;
			this->particule[p].time_sample = new int[this->nsample];
			for (int k=0;k<this->nsample;k++) this->particule[p].time_sample[k] = time_sample[k];
			this->particule[p].eventlist = new EventC [nevent];
			for (int kloc=0;kloc<nevent;kloc++){
				this->particule[p].eventlist[kloc].time = eventlist[kloc].time;
				if (eventlist[kloc].time<0) {this->particule[p].eventlist[kloc].stime = eventlist[kloc].stime;}
				this->particule[p].eventlist[kloc].action = eventlist[kloc].action;
				this->particule[p].eventlist[kloc].pop = eventlist[kloc].pop;
				this->particule[p].eventlist[kloc].pop1 = eventlist[kloc].pop1;
				this->particule[p].eventlist[kloc].pop2 = eventlist[kloc].pop2;
				this->particule[p].eventlist[kloc].sample = eventlist[kloc].sample;
				this->particule[p].eventlist[kloc].Ne = eventlist[kloc].Ne;
				if (eventlist[kloc].Ne<0) {this->particule[p].eventlist[kloc].sNe = eventlist[kloc].sNe;}
				this->particule[p].eventlist[kloc].admixrate = eventlist[kloc].admixrate;
				if ((eventlist[kloc].admixrate<0)and(eventlist[kloc].action==3)) {this->particule[p].eventlist[kloc].sadmixrate = eventlist[kloc].sadmixrate;}
				this->particule[p].eventlist[kloc].numevent0 = eventlist[kloc].numevent0;
				}
		}
		delete []eventlist;
		delete []time_sample;
		//cout << "fin normale de setevents\n";
	}


	void setparamn0(vector<int>hpi,vector<double>hpd,vector<string>hps) {
		PriorC *prior;
		Ne0C *ne0;
		int *category;
		string *name;
		double *value;
		int *paramvar;
		int ni=-1,nd=-1,ns=-1;
		int nparam,nparamvar=0,nn0;
		ni++;nparam = hpi[ni];
		prior = new PriorC[nparam];
		category = new int[nparam];
		name = new string[nparam];
		value = new double[nparam];
		paramvar =new int[nparam];
		for (int k=0;k<nparam;k++){
			ni++;category[k] = hpi[ni];
			ns++;name[k] = hps[ns];
			nd++;value[k] = hpd[nd];
			if (value[k]<0.0){
				ns++;prior[k].loi = hps[ns];
				nd++;prior[k].mini =hpd[nd];
				nd++;prior[k].maxi =hpd[nd];
				if (prior[k].maxi!=prior[k].mini) {paramvar[nparamvar]=k;nparamvar++;prior[k].constant=false;}
				else prior[k].constant=true;
				nd++;prior[k].mean = hpd[nd];
				nd++;prior[k].sdshape = hpd[nd];
				ni++;prior[k].ndec = hpi[ni];
			} else prior[k].constant=true;
		}
		ni++;nn0 = hpi[ni];
		ne0 = new Ne0C[nn0];
		for (int k=0;k<nn0;k++) {
			ni++;ne0[k].val = hpi[ni];
			ns++;ne0[k].name =hps[ns];
		}
		for (int p=0;p<this->npart;p++) {
			this->particule[p].nparamvar=nparamvar;
			this->particule[p].paramvar = new int[nparamvar];
			for(int i=0;i<nparamvar;i++)this->particule[p].paramvar[i] =paramvar[i];
			this->particule[p].nparam = nparam;
			this->particule[p].parameterlist = new HistParameterC [nparam];
			for (int k=0;k<nparam;k++){
				this->particule[p].parameterlist[k].category = category[k];
				this->particule[p].parameterlist[k].name = name[k];
				this->particule[p].parameterlist[k].value = value[k];
				//if (p==0) cout << this->particule[p].parameterlist[k].name << "  " << this->particule[p].parameterlist[k].value << "  " << this->particule[p].parameterlist[k].category <<"   ";
				this->particule[p].parameterlist[k].prior.constant = prior[k].constant;
				if (not prior[k].constant) {
					this->particule[p].parameterlist[k].prior.loi = prior[k].loi;
					//if (p==0) cout << this->particule[p].parameterlist[k].prior.loi << "  [";
					this->particule[p].parameterlist[k].prior.mini =prior[k].mini;
					//if (p==0) cout << this->particule[p].parameterlist[k].prior.mini << "  ";
					this->particule[p].parameterlist[k].prior.maxi =prior[k].maxi;
					//if (p==0) cout << this->particule[p].parameterlist[k].prior.maxi << "  ";
					this->particule[p].parameterlist[k].prior.mean = prior[k].mean;
					//if (p==0) cout <<this->particule[p].parameterlist[k].prior.mean << "  ";
					this->particule[p].parameterlist[k].prior.sdshape = prior[k].sdshape;
					//if (p==0) cout << this->particule[p].parameterlist[k].prior.sdshape << "  ";
					this->particule[p].parameterlist[k].prior.ndec = prior[k].ndec;
					//if (p==0) cout <<this->particule[p].parameterlist[k].prior.ndec <<	"]\n";
				}
			}
			this->particule[p].nn0 = nn0;
			//if (p==0) cout  << "\nnombre de Ne = " << this->particule[p].nn0 <<"\n";
			this->particule[p].ne0list = new Ne0C[nn0];
			for (int k=0;k<nn0;k++){
				this->particule[p].ne0list[k].val = ne0[k].val;
				this->particule[p].ne0list[k].name = ne0[k].name;
				//if (p==0) cout << this->particule[p].ne0list[k].name <<"   " << this->particule[p].ne0list[k].val << "\n";
			}
		}
		delete []prior;
		delete []ne0;
		delete []category;
		delete []name;
		delete []value;
		delete []paramvar;
	}

/*	void printevents() {
		std::cout << "printevents : " << this->nevent << "\n";
		for (int kloc=0;kloc<this->nevent;kloc++){
			std::cout << "event " << kloc << "\n";
			if (this->eventlist[kloc].action  == 0)
			{std::cout << this->eventlist[kloc].time << "  SAMPLE   pop=" << this->eventlist[kloc].pop << "   sample =" << this->eventlist[kloc].sample << "  numevent0 =" << this->eventlist[kloc].numevent0 << "\n";}
			else if (this->eventlist[kloc].action  == 1)
			{std::cout << this->eventlist[kloc].time << "  VARNE    pop=" << this->eventlist[kloc].pop << "   Ne =" << this->eventlist[kloc].Ne << "  numevent0 =" << this->eventlist[kloc].numevent0 << "\n";}
			else if (this->eventlist[kloc].action  == 2)
			{std::cout << this->eventlist[kloc].time << "  MERGE    pop=" << this->eventlist[kloc].pop << "   pop1 =" << this->eventlist[kloc].pop1 << "  numevent0 =" << this->eventlist[kloc].numevent0 << "\n";}
			else if (this->eventlist[kloc].action  == 3)
			{std::cout << this->eventlist[kloc].time << "  SPLIT    pop=" << this->eventlist[kloc].pop << "   pop1 =" << this->eventlist[kloc].pop1 << "   pop2 =" << this->eventlist[kloc].pop2 << " admixrate =" << this->eventlist[kloc].admixrate << "  numevent0 =" << this->eventlist[kloc].numevent0 << "\n";}

			}
		}
*/

/*
	list gethaplostate(int loc) {
		list state;
//		for (int i=0;i<)
//		return this->locuslist[loc].haplostate;
		return state;
	}

	list gethaplodna(int loc) {
		list dna;
//		return this->locuslist[loc].haplodna;
		return dna;
	}
*/
	void cleanParticle(int ipart){
		for (int loc=0;loc<this->particule[ipart].nloc;loc++) {
			if (this->particule[ipart].locuslist[loc].type>4) {
				delete []this->particule[ipart].locuslist[loc].mutsit;
			    delete []this->particule[ipart].locuslist[loc].tabsit;
			}
			delete []this->particule[ipart].locuslist[loc].haplostate;
			for(int sa=0;sa<this->particule[ipart].data.nsample;sa++) {
				if (this->particule[ipart].locuslist[loc].type<5) delete []this->particule[ipart].locuslist[loc].haplomic[sa];
				if (this->particule[ipart].locuslist[loc].type>4) delete []this->particule[ipart].locuslist[loc].haplodna[sa];
				delete []this->particule[ipart].locuslist[loc].freq[sa];
			}
			if (this->particule[ipart].locuslist[loc].type<5) delete []this->particule[ipart].locuslist[loc].haplomic;
			if (this->particule[ipart].locuslist[loc].type>4) delete []this->particule[ipart].locuslist[loc].haplodna;
			delete []this->particule[ipart].locuslist[loc].ss;
			delete []this->particule[ipart].locuslist[loc].samplesize;
			delete []this->particule[ipart].locuslist[loc].freq;
		}
		delete []this->particule[ipart].locuslist;
		for (int gr=0;gr<this->particule[ipart].ngr;gr++) delete []this->particule[ipart].grouplist[gr].loc;
		delete []this->particule[ipart].grouplist;
		delete []this->particule[ipart].data.nind;
		for(int sa=0;sa<this->particule[ipart].data.nsample;sa++) delete []this->particule[ipart].data.indivsexe[sa];
		delete []this->particule[ipart].data.indivsexe;
		delete []this->particule[ipart].stat;
		delete []this->particule[ipart].eventlist;
		delete []this->particule[ipart].ne0list;
		delete []this->particule[ipart].seqlist;
		delete []this->particule[ipart].paramvar;
		delete []this->particule[ipart].parameterlist;
		delete []this->particule[ipart].time_sample;
	}

	void cleanParticleSet(){
		for (int i=0;i<this->npart;i++) this->cleanParticle(i);
		delete []this->particule;
		for (int loc=0;loc<this->nloc;loc++) {if (this->locuslist[loc].type>4)   delete []this->locuslist[loc].mutsit;}
		delete []this->locuslist;
		for (int gr=0;gr<this->ngr;gr++) delete []this->grouplist[gr].loc;
		delete []this->grouplist;
		delete []this->nind;
		for (int i=0;i<this->nsample;i++) delete[]this->indivsexe[i];
		delete []this->indivsexe;
	}

	vector<double> dosimultabref(int npart, bool dnatrue)
		{
		//cout << "debut de dosimultabref\n";
		Header header;
		header.readHeader();
		this->npart = npart;
		this->particule = new ParticleC[this->npart];
		//cout << "apres le new ParticleC\n";
		for (int p=0;p<this->npart;p++) {
			this->particule[p].dnatrue = dnatrue;
			this->setdata(p);
			this->setgroup(p);
		}
		this->setdataloc(va,vb01,vb02,vb03,vb1,vb2);
		//cout << "apres setdataloc\n";
		this->setparamn0(vc1,vc2,vc3);
		//cout << "apres setparamn0\n";
		this->setevents(vd1,vd2,vd3);
		//cout << "apres setevents\n";
		this->setstat(ve);
		//cout << "apres setstat\n";
		int ipart,tid=0,jpart=0;
		vector<int> sOK;
		sOK.resize(this->npart);
		vector<double> paramstat;
		//cout << "avant pragma\n";
//debut du pragma
#pragma omp parallel for shared(sOK) private(ipart,tid) schedule(static)
		for (ipart=0;ipart<this->npart;ipart++){
			tid = omp_get_thread_num();
			sOK[ipart]=this->particule[ipart].dosimulpart(ipart,tid);
			//cout << "\nretour de dosimulpart sOK["<<ipart<<"] = "<<sOK[ipart] <<"\n";
			if (sOK[ipart]==0) {this->particule[ipart].docalstat();
			//cout << "retour de docalstat \n";
			}
		}
//fin du pragma
		//cout << "remplissage de paramstat \n";
		int ips=1;for (int i=0;i<this->npart;i++) {if (sOK[i]==0) {ips +=2+this->particule[i].nparamvar+this->particule[i].nstat;jpart++;}}
		//paramstat = new double[ips];

		paramstat.push_back((double)jpart);ips=1;
		for (int i=0;i<this->npart;i++) {
			if (sOK[i]==0){
			paramstat.push_back((double)this->particule[i].nparamvar);ips++;
			for (int j=0;j<this->particule[i].nparam;j++) {if (not this->particule[i].parameterlist[j].prior.constant)   paramstat.push_back(this->particule[i].parameterlist[j].value);ips++;}
			paramstat.push_back((double)this->particule[i].nstat);ips++;
			for (int j=0;j<this->particule[i].nstat;j++) {paramstat.push_back(this->particule[i].stat[j].val);ips++;}
			}
		}
		//cout <<"fin du remplissage \n";
		cleanParticleSet();
		//cout << "fin de dosimultabref\n";
		return paramstat;
	}

	list getsumstat(){
//		cout << "npart = " << this->npart << "   nstat = " << this->particule[0].nstat << "\n";
		list stat;
		for (int ipart=0;ipart<this->npart;ipart++) {
			for (int j=0;j<this->particule[ipart].nstat;j++) {
				cout << "stat[" << ipart;
				cout << "][" << j;
				cout << "] = " ;
				cout << this->particule[ipart].stat[j].val;
				cout << "\n";
				stat.append(this->particule[ipart].stat[j].val);
			}
		}
		return stat;
	}

	void setoneloci(list loc_i) {
		this->particule[0].nloc = extract<int>(loc_i[0]);
//		cout <<"nloc="<<this->particule[0].nloc<<"\n";
		this->particule[0].locuslist = new LocusC[nloc];
		int n = 0;
		for (int kloc=0;kloc<this->particule[0].nloc;kloc++){
			n +=1;
			this->particule[0].locuslist[kloc].type =extract<int>(loc_i[n]);
			if (this->particule[0].locuslist[kloc].type < 5) {
				n +=1;this->particule[0].locuslist[kloc].kmin = extract<int>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].kmax = extract<int>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].motif_size = extract<int>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].motif_range = extract<int>(loc_i[n]);
				}
			else {
				n +=1;this->particule[0].locuslist[kloc].dnalength = extract<int>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].p_fixe = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].gams = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].mus_rate = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].k1 = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].k2 = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].mutmod = extract<int>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].pi_A = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].pi_C = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].pi_G = extract<double>(loc_i[n]);
				n +=1;this->particule[0].locuslist[kloc].pi_T = extract<double>(loc_i[n]);
				this->particule[0].locuslist[kloc].mutsit = new double[locuslist[kloc].dnalength];
				for (int i=0;i<this->particule[0].locuslist[kloc].dnalength;i++) {
					n +=1;this->particule[0].locuslist[kloc].mutsit[i] = extract<double>(loc_i[n]);
					//std::cout << locuslist[kloc].mutsit[i]<< "   ";
					}
				//std::cout <<"\n";
				}
			double coeff=0.0;
//			cout << "sex-ratio = " << this->sexratio << "\n";
			switch (this->particule[0].locuslist[kloc].type % 5)
			{	case 0 :  coeff = 16.0*this->sexratio*(1.0-this->sexratio);break;
				case 1 :  coeff = 2.0;break;
				case 2 :  coeff = 18.0*this->sexratio*(1.0-this->sexratio)/(1.0+this->sexratio);break;
				case 3 :  coeff = 2.0*this->sexratio;break;
				case 4 :  coeff = 2.0*(1.0-this->sexratio);break;
			}
			this->particule[0].locuslist[kloc].coeff=coeff;
//			cout << "locus " << kloc << "   type=" << this->particule[0].locuslist[kloc].type << "   coeff=" << this->particule[0].locuslist[kloc].coeff << "\n";
		}
	}

	void sethaplo(list haplo) {
		int n=0;
		for (int loc=0;loc<this->particule[0].nloc;loc++){
			this->particule[0].locuslist[loc].ss = new int[this->nsample];
			this->particule[0].locuslist[loc].samplesize = new int[this->nsample];
			for (int sa=0;sa<this->nsample;sa++) {
				this->particule[0].locuslist[loc].ss[sa]=extract<int>(haplo[n]);n++;
//				cout << this->particule[0].locuslist[loc].ss[sa]<<", ";
			}
		}
//		cout << "\n";
		for (int loc=0;loc<this->particule[0].nloc;loc++){
			this->particule[0].locuslist[loc].haplomic = new int*[this->nsample];
			for (int sa=0;sa<this->nsample;sa++) {
				this->particule[0].locuslist[loc].samplesize[sa]=0;
				this->particule[0].locuslist[loc].haplomic[sa] = new int[this->particule[0].locuslist[loc].ss[sa]];

				for (int i=0;i<this->particule[0].locuslist[loc].ss[sa];i++) {
					this->particule[0].locuslist[loc].haplomic[sa][i] = extract<int>(haplo[n]);n++;
					if (this->particule[0].locuslist[loc].haplomic[sa][i]!=MISSING) this->particule[0].locuslist[loc].samplesize[sa]++;

				}
//				cout <<"samplesize["<<loc<<"]["<<sa<<"]="<< this->particule[0].locuslist[loc].samplesize[sa]<<"\n";
			}
		}

	}

	void setonepart(list da, list loci,list haplo) {
		setdata(da);
		setoneloci(loci);
		sethaplo(haplo);
	}

	list getonestat(){
//		cout << "npart = " << this->npart << "   nstat = " << this->particule[0].nstat << "\n";
		this->particule[0].docalstat();
		list stat;
		for (int j=0;j<this->particule[0].nstat;j++) stat.append(this->particule[0].stat[j].val);
		return stat;
	}


};

//BOOST_PYTHON_MODULE(simuldatC)
//{
//	class_<ParticleSetC>("ParticleSet")
////		.def("setdnatrue", &ParticleSetC::setdnatrue)
////		.def("setevents", &ParticleSetC::setevents)
//		.def("dosimultabref", &ParticleSetC::dosimultabref)
//		.def("gethaplostate", &ParticleSetC::gethaplostate)
//		.def("gethaplodna", &ParticleSetC::gethaplodna)
////		.def("setstat", &ParticleSetC::setstat)
////		.def("setdataloc", &ParticleSetC::setdataloc)
////		.def("setparamn0", &ParticleSetC::setparamn0)
////		.def("setnpart", &ParticleSetC::setnpart)
//		.def("getsumstat", &ParticleSetC::getsumstat)
//		.def("setonepart",  &ParticleSetC::setonepart)
//		.def("getonestat", &ParticleSetC::getonestat)
//    ;
//}

/*void do_main(int npart) {
	int a[]={3, 30, 30, 30, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2};
	vector <int> va;
	va.assign(a,a+94);
	int b01[]={2,0,5,0,1,2,3,4,6,3,0,5,5,6,7,8,9};
	vector <int> vb01;
	vb01.assign(b01,b01+17);
	double b02[]={-1.0,0.0001,0.001,-1.0,-1.0,-1.0,0.01,0.3,-1.0,-1.0,0.0,0.0005,0.22,0.0};
	vector<double> vb02;
	vb02.assign(b02,b02+14);
	vector <string> vb03;
	vb03.resize(2);vb03[0]="UN";vb03[1]="UN";


	int    b1[]={10, 0, 0, 100, 180, 2, 40, 0, 2, 200, 280, 2, 40, 0, 4, 100, 180, 2, 40,  0, 0, 200, 280, 2, 40,  0, 0, 100, 180, 2, 40,  1, 0, 200, 280, 2, 40, 1, 0, 100, 180, 2, 40,  1, 0, 200, 280, 2, 40, 1, 0, 200, 280, 2, 40,1,0,200,280,2,40};
	vector <int> vb1;
	vb1.assign(b1,b1+61);
	double b2[]={ -1.0,0.00001,0.01,2.0,-1.0,0.01,0.5,2.0, 0.0,
			      -1.0,0.00001,0.01,2.0,-1.0,0.01,0.5,2.0, 0.0,
			      -1.0,0.00001,0.01,2.0,-1.0,0.01,0.5,2.0, 0.0,
			      -1.0,0.00001,0.01,2.0,-1.0,0.01,0.5,2.0, 0.0,
			      -1.0,0.00001,0.01,2.0,-1.0,0.01,0.5,2.0, 0.0,
			      0.0005,0.22,0.0,0.0005,0.22,0.0,0.0005,0.22,0.0,0.0005,0.22,0.0,0.0005,0.22,0.0};
	vector<double> vb2;
	vb2.assign(b2,b2+60);

	int    c1[]={8,0,0,0,0,0,0,1,0,1,0,0,0,2,4,1,0,3,-1,-1,-1};
	vector <int> vc1;
	vc1.assign(c1,c1+21);
	double c2[]={-1.0,1000.0,20000.0,0.0,0.0,-1.0,1000.0,20000.0, 0.0,0.0,-1.0,1000.0,20000.0,0.0,0.0,-1.0,100.0,1000.0,0.0,0.0,-1.0,1.0,10.0,0.0,0.0,-1.0,8.0,80.0,0.0,0.0,-1.0,0.001,0.999,0.0,0.0,-1.0,1000.0,100000.0,0.0,0.0};
	vector<double> vc2;
	vc2.assign(c2,c2+40);
	vector <string> vc3;
	vc3.resize(19);
	for (int i=0;i<8;i++){vc3[2*i+1]="UN";}
	vc3[0]="N1";vc3[2]="N2";vc3[4]="N3";vc3[6]="t1";vc3[8]="db";vc3[10]="Nb";vc3[12]="lambda";vc3[14]="t2";vc3[16]="N1";vc3[17]="N2";vc3[18]="N3";

	int    d1[]={6, 2, 0, 1, -1, -1, 1, -1,  0, 0, 0, 2, -1, -1, 2, -1, 1, 4, 0, 3, -1, -1, 3, -1,  2, -1, 1, 2, -1, -1, -1, -1,   3, -1,  3, 3, 1, 2, -1, -1, 4, -1, 2, 1, 2, -1, -1, -1, 5};
	vector <int> vd1;
	vd1.assign(d1,d1+49);
	double d2[]={-1.0,-1.0,-1.0,-1.0, -1.0, -1.0};
	vector<double> vd2;
	vd2.assign(d2,d2+6);
	vector <string> vd3;
	vd3.resize(10);
	vd3[0]="N1";vd3[1]="N2";vd3[2]="N3";vd3[3]="t1-db";vd3[4]="Nb";vd3[5]="t1";vd3[6]="N3";vd3[7]="lambda";vd3[8]="t2";vd3[9]="N1";

	int e[]={20, 1, 0, 0, 0, 0,
				 1, 1, 0, 0, 0,
				 1, 2, 0, 0, 0,
				 2, 0, 0, 0, 0,
				 2, 1, 0, 0, 0,
				 2, 2, 0, 0, 0,
				 3, 0, 0, 0, 0,
				 3, 1, 0, 0, 0,
				 3, 2, 0, 0, 0,
				 4, 0, 0, 0, 0,
				 4, 1, 0, 0, 0,
				 4, 2, 0, 0, 0,
				 5, 0, 2, 0, 1,
				 6, 0, 2, 0, 1,
				 7, 0, 2, 0, 1,
				 8, 0, 2, 0, 1,
				 9, 0, 2, 0, 1,
				 10, 0, 2, 0, 1,
				 11, 0, 2, 0, 1,
				 12, 2, 0, 1, 1};
	vector <int> ve;
	ve.assign(e,e+101);

	ParticleSetC pc;
	vector<double> resu;
	resu = pc.dosimultabref(npart, false, va,vb01,vb02,vb03,vb1,vb2,vc1,vc2,vc3,vd1,vd2,vd3,ve);
	cout << resu[0] <<" particules simulées avec succès\n";*/
}*/
