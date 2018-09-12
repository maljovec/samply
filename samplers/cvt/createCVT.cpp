#include <stdio.h>
#include <assert.h>

#include "timing.h"
#include "runUtils.h"
#include <ANN/ANN.h>

bool useAnn;

template <class T>
struct Point{
  T* x;
};

template <class T>
void allocPoint(Point<T> &p, int D){
  p.x = new T[D];
}

template <class T>
void deallocPoint(Point<T> &p){
  delete p.x;
}


template <class T>
T distance2(T *x, T *y, int D) {
  T sum = 0;
  for(int i=0;i<D;i++) {
    sum += (x[i]-y[i])*(x[i]-y[i]);
  }
  return sum;
}

template <class T>
T random(T a, T b) {
  return a + (T) rand()/(T) RAND_MAX * (b-a);
}

template <class T>
void createCVT(int N, int D, int maxIters, T epsilon, int &iters, int seed) {
  srand(seed);

  Point<T> *points = new Point<T>[N];

  for(int i=0;i<N;i++) {
    allocPoint(points[i],D);
  }

  for(int i=0;i<N;i++) {
    for(int d = 0; d<D;d++) {
      points[i].x[d] = random(0.0,1.0);
    }
  }

  int dim = D;
  int nPts = (int) N;
  fprintf(stderr, "Allocating points of size %d and dimension %d\n", nPts, dim);
  ANNpointArray dataPts;
  ANNpoint queryPt;
  ANNidxArray nnIdx;
  ANNdistArray dists;
  ANNkd_tree* kdTree;
  const int K = 1;

  dataPts = annAllocPts(nPts, dim);
  nnIdx = new ANNidx[K];
  dists = new ANNdist[K];

  for(unsigned int i = 0; i<N;i++) {
    for(int k=0;k<D;k++) {
      dataPts[i][k] = points[i].x[k];
    }
  }

  kdTree = new ANNkd_tree(dataPts, nPts, dim);
  if(nPts<1) return;

  int numIters = maxIters;
  iters = numIters;
  T *ji = new T[N];
  T *error = new T[N];
  for(int i=0;i<N;i++) {
    ji[i] = 1.0;
    error[i] = 1.0;
  }
  int maxErrorId = -1;
  T maxError = 0.0;
  Point<T> p;
  allocPoint(p,D);
  for(int i=0;i<numIters;i++) {
    if(i%10000==0) { fprintf(stderr,"Iter %d err = %lg\n", i, sqrt(maxError)); fflush(stderr); }
    for(int d = 0; d<D;d++) {
      p.x[d] = random(0.0,1.0);
    }

    // find closest
    int closest=-1;
    if(useAnn) {
      queryPt = annAllocPt(D);
      for(int k=0;k<D;k++) queryPt[k] = p.x[k];
      kdTree->annkSearch(queryPt, K, nnIdx, dists);
      closest = nnIdx[0];

      annDeallocPt(queryPt);

    } else {
      T minD=1e3;
      int closest2=-1;
      for(unsigned int j=0;j<N;j++) {
    T d2 = distance2<T>(p.x, points[j].x,D);
    if(d2<minD || j==0) {
      minD = d2;
      closest2=j;
    }
      }
      closest = closest2;
    }

//#define SANITY_CHECK
#ifdef SANITY_CHECK
      if(closest!=closest2 && closest>=0) {
    printf("%f-%f Closest(ANN) = %d d=%f closest2 = %d d=%f\n", p.x[0], p.x[1],  closest, distance2(p.x, points[closest].x,D), closest2, distance2(p.x, points[closest2].x, D));
      }
      //assert(closest==closest2);
#endif

    if(closest>=N) continue;
    assert(closest>=0);

    T sumdiff = 0;
    for(int d = 0; d<D;d++) {
      T px = points[closest].x[d];
      points[closest].x[d] = (ji[closest]*points[closest].x[d] + p.x[d])/(ji[closest]+1);
      T diffx = px - points[closest].x[d];
      sumdiff+=diffx*diffx;
    }

    for(int k=0;k<D;k++) {
      dataPts[closest][k] = points[closest].x[k];
    }

    if(i%10000==0) {
      delete kdTree;
      // re-create Kd tree to be on the safe side
      // assuming ANN does not update it
      kdTree = new ANNkd_tree(dataPts, nPts, dim);
    }

    ji[closest]=ji[closest]+1;

    if(epsilon>0) {
      error[closest] = (sumdiff);

      /*
      maxError = 0.0;
      for(unsigned int j=0;j<N;j++) {
    maxError = (error[j]<2.0)? fmax(maxError, error[j]): maxError;
      }
      */
      // Approximation of the max.error without the need to traverse all points
      if(maxErrorId==closest) {
    maxError = error[closest];
      } else if(error[closest]>maxError) {
    maxErrorId = closest;
    maxError = error[closest];
      }

      if(maxError<epsilon*epsilon) {
    iters = i;
    fprintf(stderr,"Converged at %d err = %lg\n", i, sqrt(maxError));
    break;
      }
    }

  }

  /****************************/
  /* Compute maximin distance */
  /****************************/
  delete kdTree;
  T maximinDistSqr = 0;

  // re-create Kd tree to be on the safe side
  kdTree = new ANNkd_tree(dataPts, nPts, dim);

  int K0 = 2;
  ANNidx *nnIdx0 = new ANNidx[K0];
  ANNdist *dists0 = new ANNdist[K0];
  for(unsigned int j=0;j<N;j++) {
    queryPt = annAllocPt(D);
    for(int k=0;k<D;k++) queryPt[k] = points[j].x[k];
    kdTree->annkSearch(queryPt, K0, nnIdx0, dists0);
    int closest = nnIdx0[1];
    annDeallocPt(queryPt);
    T dist2 = distance2(points[j].x, points[closest].x, D);
    maximinDistSqr = fmax(maximinDistSqr, dist2);
  }

  deallocPoint(p);
  fprintf(stderr,"maximin distance = %lg\n", sqrt(maximinDistSqr));
  delete ji;
  delete error;
  delete kdTree;


  // Output points to stdout
  for(unsigned int i=0;i<N;i++) {
    for(int d = 0; d<D;d++) {
      fprintf(stdout, "%.9g ", points[i].x[d]);
    }
    fprintf(stdout, "\n");
  }
  fclose(stdout);

  for(int i=0;i<N;i++) {
    deallocPoint(points[i]);
  }
  delete[] points;
}

int main(int argc, char *argv[]) {
  addArgument("-N", "1000", "Number of points");
  addArgument("-D", "2", "Number of dimensions");
  addArgument("-iterations", "10000", "Max. Number of iterations");
  addArgument("-epsilon", "1e-5", "Epsilon (max. CVT error)\n\twhen epsilon<0, run for #iterations");
  addArgument("-ann", "1", "1: Use ANN (lazy update) --  0: Brute force search");
  addArgument("-seed", "333", "Random seed");
  // Read arguments
  processArgs(argc, argv);
  if(argc<4) {
    fprintf(stderr, "Usage:\n %s :\n", argv[0]);
    printArguments();
    exit(0);
  }

  int N = getArgInt("-N");
  int D = getArgInt("-D");
  double epsilon = (double) getArgFloat("-epsilon");
  int iters = getArgInt("-iterations");
  int numIters;
  int seed = getArgInt("-seed");
  useAnn = getArgInt("-ann")==1;

  timestamp t = now();
  createCVT<double>(N,D,iters, epsilon, numIters, seed);
  timestamp t2 = now();

  fprintf(stderr, "Elapsed time = %f s.\n", t2-t);

}
