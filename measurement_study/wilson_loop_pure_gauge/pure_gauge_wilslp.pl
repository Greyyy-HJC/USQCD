#!/usr/bin/perl

## ======================================================= ##
## ================== PARAMETERS INPUT =================== ##
## ======================================================= ##

### check params num ###
$num_args = $#ARGV + 1;
if ($num_args != 1) { #check 输入参数是否为2，如果不是，则直接中断pl
   exit;
}
$conf_num=$ARGV[0];

## ======================================================= ##
## ================= CONFIGURATION INFO ================== ##
## ======================================================= ##
$ns=16;
$nt=16;

$cfg_type="SZINQIO";
$cfg_file="../../config/pure_gauge/pure_gauge_S16_T16_beta6.lime${conf_num}";

## ======================================================= ##
## ===================== XML FILE HEAD =================== ##
## ======================================================= ##

print <<"EOF";
<?xml version="1.0"?>
<chroma>
  <annotation>
  Calculate the Wilson loop
  </annotation>
  <Param>
    <InlineMeasurements>
EOF

## ======================================================= ##
## ======================== WILSLP ======================= ##
## ======================================================= ##

print <<"EOF";
      <elem>
        <!-- Wilson loops -->
        <Name>WILSLP</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>3</version>
          <kind>2</kind>
          <j_decay>3</j_decay>
          <t_dir>3</t_dir>
        </Param>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
        </NamedObject>
      </elem>
EOF

## ======================================================= ##
## ===================== XML FILE TAIL =================== ##
## ======================================================= ##

print <<"EOF";
    </InlineMeasurements>
    <nrow>${ns} ${ns} ${ns} ${nt}</nrow>
  </Param>
  <Cfg>
    <cfg_type>${cfg_type}</cfg_type>
    <cfg_file>${cfg_file}</cfg_file>
    <!-- pure gauge config -->
  </Cfg>
</chroma>
EOF

## ======================================================= ##
## ==================== XML FILE END ===================== ##
## ======================================================= ##