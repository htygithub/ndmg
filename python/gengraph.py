#
#
# Read a fiber file and generate the corresponding sparse graph
#
#

import argparse
import sys
from fibergraph import FiberGraph
from fiber import FiberReader


#
# 
#
def genGraph( infname, outfname, numfibers ):

    # Create fiber reader
    reader = FiberReader( infname )

    # Create the graph object
    # get dims from reader
    fbrgraph = FiberGraph ( reader.shape )


    # Print the high-level fiber information
    print(reader)

    count = 0

    # first pass finds the seed locations (vertices)
    for fiber in reader:
      count += 1
      fbrgraph.addVertex ( fiber )
      if numfibers > 0 and count >= numfibers:
        break
      if count % 1000 == 0:
        print ("Found vertices of {0} fibers".format(count) )

    count = 0

    # iterate over all fibers
    for fiber in reader:
      count += 1
      # add the contribution of this fiber to the 
      fbrgraph.add(fiber)
      if numfibers > 0 and count >= numfibers:
        break
      if count % 1000 == 0:
        print ("Processed {0} fibers".format(count) )

    # Done adding edges
    fbrgraph.complete()

    # Save a version of this graph to file
    fbrgraph.saveToMatlab ( "fibergraph", outfname )

    # Load a version of this graph from  
    fbrgraph.loadFromMatlab ( "fibergraph", outfname )

    # output graph to SciDB ingest format
#    fbrgraph.writeForSciDB( [65536,65536], fout )

    del reader

    return



#
# main
#
def main ():
    parser = argparse.ArgumentParser(description='Read the contents of MRI Studio file and generate a sparse connectivity graph in SciDB.')
    parser.add_argument('--count', action="store", type=int, default=-1)
    parser.add_argument('file', action="store")
    parser.add_argument('output', action="store")

    result = parser.parse_args()
    genGraph ( result.file, result.output, result.count )

if __name__ == "__main__":
      main()