// $Id: spectrum_w.cc,v 1.49 2005/03/25 15:28:04 flemingg Exp $
/*! \file
 * \brief Main code for spectrum measurements
 */

#include "chroma.h"

using namespace QDP;
using namespace Chroma;
using std::string;
using std::endl;
using std::flush;

/* Linkage */

/*
 * Input 
 */
// Parameters which must be determined from the XML input
// and written to the XML output
struct Param_t
{
  multi1d<int> nrow; // array of lattice dimensions
  std::string myname; // Exercise: add my name 
};


//! Propagators
struct Prop_t
{
  std::string prop_file;  // The files are expected to be in SciDAC format! // this is the name of the propagator file
};


//! Mega-structure of parameters
struct App_input_t
{
  Param_t          param;
  Cfg_t            cfg;
  Prop_t           prop;
};


//! XML READ THE PROP STRUCT
void read(XMLReader& xml, const string& path, Prop_t& input) // same name but different third argument, it is called function overloading
{
  XMLReader inputtop(xml, path);
  read(inputtop, "prop_file", input.prop_file);
} // read the name of the propagator file from xml file to prop_t struct
// inputtop is the xml reader, including outer tags, "prop_file" is the tag in the xml file, input.prop_file is the variable in the prop_t struct


//! XML READ THE PARAM STRUCT
void read(XMLReader& xml, const string& path, Param_t& param)
{
  XMLReader paramtop(xml, path);
  read(paramtop, "nrow", param.nrow);
  read(paramtop, "myname", param.myname);
}

// Cfg reader already defined in param/IO

// Reader recursively all the input Param, Cfg_t, Prop
void read(XMLReader& xml, const string& path, App_input_t& input)
{
  XMLReader inputtop(xml, path);

  // Read all the input groups
  try
  {
    // Read program parameters
    read(inputtop, "Param", input.param);

    // Read in the gauge configuration info
    read(inputtop, "Cfg", input.cfg);

    // Read in the propagator(s) info
    read(inputtop, "Prop", input.prop);
  }
  catch (const string& e)  // Catch any exceptions/errors
  {
    QDPIO::cerr << "Error reading prop data: " << e << endl;
    QDP_abort(1);
  }
}


//
// Main program
//
int main(int argc, char **argv)
{
  // Put the machine into a known state
  Chroma::initialize(&argc, &argv);
  
  // Put this in to enable profiling etc.
  START_CODE();  // On line 94, there is a function call START_CODE() paired with a function END_CODE() on line 220. These functions invoke the profiling functionality of QDP++ if that has been enabled. You are encouraged to put START_CODE() and END_CODE() calls in later functions that you may write yourself.

  // Input parameter structure
  App_input_t  input;

  // Instantiate xml reader for DATA
  // if you used -i input file, Chroma::getXMLInputFileName() returns
  //  the filename you specified
  // otherwise it will return "DATA"
  XMLReader xml_in;
  try { 
    xml_in.open(Chroma::getXMLInputFileName());
  }
  catch(...) { // Catch ALL Exceptions
    QDPIO::cerr << "Could not open input XML file: " 
		<< Chroma::getXMLInputFileName() 
		<< endl;
    QDP_abort(1);  // Semi Graceful exit.
  }

  // Terminal I/O to stdout.
  QDPIO::cout << "Hello World" << endl;  // Using this special QDPIO::cout on a parallel machine will result only in 1 processor writing to the terminal.

  // Read data: Call top level reader, fill out the structure.
  // Root tag must be <tutorial2>
  read(xml_in, "/tutorial2", input);

  // Set lattice size, shape, etc.
  // using the nrow param from the Prameter structure
  Layout::setLattSize(input.param.nrow);

  // Initialise
  Layout::create();
  
  // -------------------------------------------------------------------
  // Read in the configuration along with relevant information.
  // -------------------------------------------------------------------

  // The gauge field may contain some file XML and other 
  // information (gauge XML): eg in the future the ILDG header(?)
  // We create empty XML readers for this, the gauge reading routine
  // will fill them in
  XMLReader gauge_file_xml, gauge_xml;

  // The gauge field itself
  multi1d<LatticeColorMatrix> u(Nd);
  

  // A convenience routine to read various gauge field formats
  gaugeStartup(gauge_file_xml, gauge_xml, u, input.cfg);

  // Check if the gauge field configuration is unitarized
  unitarityCheck(u);
  // ---------------- Gauge Reading Done -------------------------------


  // ---------------- Read in a propagator -----------------------------

  // Propagator also contains headers: a file XML and a record XML
  // as well as the binary data -- as dictated by SciDAC standards
  // the propagator code now only dumps SciDAC props.
  XMLReader prop_file_xml, prop_record_xml;

  // The propagator itself
  LatticePropagator quark_propagator;
 
  QDPFileReader prop_reader(prop_file_xml,
			    input.prop.prop_file,     
			    QDPIO_SERIAL);

  prop_reader.read(prop_record_xml, quark_propagator);

  prop_reader.close();

  // --------------- Propagator reader done ---------------------------

  // Instantiate XML writer for XMLDAT
  // Chroma::getXMLOutputInstance() returns an XMLFileWriter reference
  // If you gave chroma the command line option:
  //  -o output_xml_file   then output_xml_file is opened 
  //  if you gave no command line option then "XMLDAT" is opened
  XMLFileWriter& xml_out = Chroma::getXMLOutputInstance();

  // Enter group under tag <tutorial3>. This is the first push() making
  // this the root tag.
  push(xml_out, "tutorial2"); // open a root tag called tutorial2

  proginfo(xml_out);    // Print out basic program info (writes own 
                        // surrounding tags.

  // Write out the output: 
  //  Note: you can write out the contents of an entire reader.
  //  Here the contents of the reader will go in a group surrounded
  //  with tags <Input> </Input>

  //  If you don't want extra surrounding tags you can use
  //  xml_out << xml_in
  write(xml_out, "Input", xml_in);

  // Write out the config info (same deal as above)
  write(xml_out, "Config_info", gauge_xml);

  // Exercise: Output things about the prop (from prop_record_xml)
  // Here



  // Flush buffers in case you get an error
  xml_out.flush();

  // Calculate the plaquette. This form will write it out
  // information surrounded by tag: <Plaquette> ... </Plaquette>
  MesPlq(xml_out, "Plaquette", u);
  xml_out.flush();
  pop(xml_out);

  //! Do something exciting here yourself.
  //! Suggested exercise: Compute the zero mom pion on the propagator you 
  //!                     have read.

  // C(t) = sum_{x} Tr gamma_5 \bar{G}(0,x) gamma_5 G(0,x)
  // \bar{G}(0,x) = gamma_5 G(0,x) gamma_5

  LatticePropagator anti_quark = Gamma(15) * quark_propagator * Gamma(15);

  LatticeComplex traced_props = trace( Gamma(15)*adj(anti_quark)*Gamma(15)*quark_propagator );

  SftMom phases(0, true, Nd-1); // This creates the momentum phases, with a maximum mom^2 of zero. The true argument asks for equivalent momenta to be averaged, which is not relevant in this case. The Nd-1 nominates direction Nd-1=3 as the time direction (remember these are indexed from 0).

  multi2d<DComplex> hsum; // A 2D array of double prec complex numbers 
  // One dimension is indexed by momenta
  // The other is the timeslice

  hsum = phases.sft(traced_props); // Apply the fourier transform

  // Create an XMLArrayWriter to write out am array of numMom() elements 
  XMLArrayWriter momenta(xml_out, phases.numMom()); 

  push(momenta, "PseudoScalar"); // Array will be called PseudoScalar

  // loop over all the momenta 
  for(int i=0; i < phases.numMom(); i++) { 

    // Special XMLArrayWriter instruction to start a new array element 
    push(momenta); 

    // Write out the momentum index 
    write(momenta, "mom_index", i); 

    // Write out the 3 momentum corresponding to this index 
    write(momenta, "mom", phases.numToMom(i)); 

    // Write correlator 
    write(momenta, "correlator", hsum[i]);

    // We are done with this element 
    pop(momenta);
  }

  pop(momenta); // Pop the toplevel tag 



  //! Do something exciting here yourself
  //! Suggested exercise: Create a linear operator and apply it
  //! to a gaussian noise vector.

  typedef QDP::LatticeFermion T; 
  typedef QDP::multi1d<LatticeColorMatrix> P; 
  typedef QDP::multi1d<LatticeColorMatrix> Q; 

  // Parameters for boundary conditions 
  SimpleFermBCParams bc_params; 

  bc_params.boundary.resize(Nd); 
  for(int i=0; i < Nd-1; i++) { 
    bc_params.boundary[i] = BC_TYPE_PERIODIC; 
  } 
  bc_params.boundary[Nd-1] = BC_TYPE_ANTIPERIODIC; 

  // The boundary conditions themselves - we will get one from the 
  // heap using new and drop it into the handle, since that is what 
  // the CreateFermState constructor wants.
  Handle< FermBC<T,P,Q> > fbc_handle( new SimpleFermBC< T,P,Q >(bc_params) );


  // Create a FermState Creator with boundaries
  Handle<CreateFermState<T,P,Q> > cfs( new CreateSimpleFermState<T,P,Q>(fbc_handle));


  // Now create the FermAct using the FermState Creator
  EvenOddPrecWilsonFermAct S( cfs, Real(0.3));

  // Use the FermAct to create a suitable FermState
  Handle< FermState<T,P,Q> > fs( S.createState(u) );

  // Use the FermAct to create a linear Operator over the FermState
  Handle< LinearOperator<T> > M( S.linOp(fs) ); 

  // Declare the vectors
  LatticeFermion source_vector; 
  LatticeFermion target_vector; 

  // fill the source with gaussian noise
  // We use the subset method of the linear operator 
  // so we only fill the part of the vector the operator cares about

  gaussian(source_vector, M->subset()); 
  target_vector[ M->subset() ] = zero; 

  // Apply the linear operator
  (*M)(target_vector, source_vector, PLUS);

  // We already have M source. 
  // Now apply M^{\dagger} onto the target 
  // to get (M^\dagger M) source_vector 

  LatticeFermion mdagm_target_1;

  // DELIBERATE MISTAKE TO TEST THE TEST: Use PLUS instead of MINUS
  (*M)(mdagm_target_1, target_vector, MINUS); // MINUS means apply M^\dagger 

  // Now check against M^\dagger M method.
  // Create the linear operator 
  Handle< const LinearOperator<LatticeFermion> > MdM( S.lMdagM(fs) ); 

  // A target for the MdM operator
  // I will not initialize it as I would just overwrite the initialisation
  LatticeFermion mdagm_target_2; 

  // Apply the "squared" operator
  (*MdM)(mdagm_target_2, source_vector, PLUS); 

  // A vector for the difference of the 2 results 
  LatticeFermion diff; 

  // Take the difference on the subset of the linear operator
  // Note: Subset index is only on the target 
  diff[M->subset()] = mdagm_target_2 - mdagm_target_1; 

  // Compute the norm of the difference on the subset 
  // norm2() computes the squared norm. 
  Double norm_diff = sqrt(norm2(diff, M->subset())); 

  // Print the difference.
  QDPIO::cout << "LinearOperator test: norm2(diff) = " << norm_diff << endl; 

  // Check that the difference is small 
  // Note: I use the toBool() function because I am comparing QDP++
  // types rather than C++ primitive types and I have not overloaded

  if( toBool( norm_diff > Double(1.0e-5) ) ) { 
    QDPIO::cout << "LinearOperator test FAILED" << endl << flush;
    QDP_abort(1); 
  } 
  else { 
    QDPIO::cout << "LinearOperator test PASSED" << endl << flush;
  } 


  END_CODE(); // End 


  // Time to bolt
  Chroma::finalize();

  exit(0);
}
