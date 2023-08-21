#
#  $Id: regres.pl,v 3.0 2006-04-03 04:59:24 edwards Exp $
#
#  This is the portion of a script this is included recursively
#

#
# Each test has a name, input file name, output file name,
# and the good output that is tested against.
#

$top_builddir = "/home/jinchen/USQCD/install/chroma";
$test_dir = "/home/jinchen/USQCD/measurement_study/wilson_loop_pure_gauge/wilslp";

@regres_list = 
    (
     {
	 exec_path   => "$top_builddir/chroma/bin" , 
	 execute     => "chroma" , 
	 input       => "$test_dir/wilslp.ini.xml" , 
	 output      => "wilslp.candidate.xml",
	 metric      => "$test_dir/wilslp.metric.xml" ,
	 controlfile => "$test_dir/wilslp.out.xml" ,
     }
     );
