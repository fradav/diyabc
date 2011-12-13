/*
 * data.h
 *
 *  Created on: 9 déc. 2011
 *      Author: ppudlo
 */

#ifndef DATA_H_
#define DATA_H_

/**
*  Structure LocusC : définition de la structure LocusC
*/
struct LocusC
{
  string name;
  int type;  //0 à 14
  int groupe;    //numero du groupe auquel appartient le locus
  double coeffcoal;  // coefficient pour la coalescence (dépend du type de locus et du sexratio)
  long double **freq;
  //Proprietes des locus sequences
  long double pi_A,pi_C,pi_G,pi_T;
  vector <long double> mutsit;   //array of dnalength elements giving the relative probability of a mutation to a given site of the sequence
  vector <int> sitmut;   //array of nsitmut dna sites that are changed through a mutation
  vector <int> sitmut2;  //
  int dnalength,dnavar;
  vector <int> tabsit;   //array of dnalength elements giving the number of a dna site;
  string **haplodna; //array[sample][gene copy][nucleotide] tous les nucleotides de chaque individu sont mis à la suite les uns des autres
  string **haplodnavar; //seulement les sites variab
  //Proprietes des locus microsatellites
  int mini,maxi,kmin,kmax,motif_size,motif_range,nal;
  double mut_rate,Pgeom,sni_rate,mus_rate,k1,k2;
  int **haplomic; //array[sample][gene copy]
  //Propriétés des locus SNP
  bool firstime;
  short int **haplosnp; //array[sample][gene copy] 0,1,9
  bool mono;  //mono=true si un seul allèle dans l'échantillon global

  void libere(bool obs, int nsample);
};

struct MissingHaplo
{
	int locus,sample,indiv;
};

struct MissingNuc
{
	int locus,sample,indiv,nuc;
};


class DataC
{
public:
	string message,title,**indivname,***genotype;
	int nsample,nsample0,nloc,nmisshap,nmissnuc,nmisssnp,filetype;
	//int *nind;
	//int **indivsexe;
	double sexratio;
	MissingHaplo *misshap, *misssnp;
	MissingNuc   *missnuc;
	LocusC *locus;
    bool Aindivname,Agenotype,Anind,Aindivsexe,Alocus;
	//int **ss;  //nombre de copies de gènes (manquantes incluses) par [locustype][sample], locustype variant de 0 à 4.
	bool *catexist;
	vector < vector <int> > ss;//nombre de copies de gènes (manquantes incluses) par [locustype][sample], locustype variant de 0 à 4.
	vector <int> nind;
	vector < vector <int> > indivsexe;

	/* Méthodes */
	void libere();
	/**
	 * détermination du type de fichier de donnée
	 * return=-1
	 * return=0 si genepop
	 * return=1 si snp
	 */
	int testfile(string filename);
	/**
	 * lecture d'un fichier de donnée SNP et stockage des informations dans une structure DataC
	 */
	int  readfilesnp(string filename);
	/**
	 * supprime les locus monomorphes
	 */
	void purgelocmonomorphes();
	void missingdata();
	/**
	 * traitement des locus snp
	 */
	void do_snp(int loc);


	/**
	 * ecriture en binaire d'un fichier snp
	 */
	void ecribin(string filenamebin);
	/**
	 * lecture en binaire d'un fichier snp
	 */
	void libin(string filenamebin);
	/**
	 * lecture d'un fichier de donnée GENEPOP et stockage des informations dans une structure DataC
	 */
	int readfile(string filename);
	/**
	 * traitement des génotypes microsat au locus loc
	 */
	void do_microsat(int loc);
	/**
	 * traitement des génotypes DNA sequence au locus loc
	 */
	void do_sequence(int loc);
	/**
	 * calcul du coefficient dans la formule de coalescence en fonction du type de locus
	 * 0:autosomal diploide, 1:autosomal haploïde, 2:X-linked, 3:Y-linked, 4:mitochondrial
	 */
	void cal_coeffcoal(int loc);

	void calcule_ss();
	/**
	 * chargement des données dans une structure DataC
	 */
	int loadfromfile(string filename);
};



#endif /* DATA_H_ */