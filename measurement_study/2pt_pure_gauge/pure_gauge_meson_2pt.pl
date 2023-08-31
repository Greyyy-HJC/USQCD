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
# $cfg_file="../../config/pure_gauge_minhuan/quenched_test.lime${conf_num}"; #* use minhuan's config
$output_file="output_file/zero_mom_2pt.lime${conf_num}";

## ======================================================= ##
## ===================== XML FILE HEAD =================== ##
## ======================================================= ##

print <<"EOF";
<?xml version="1.0"?>
<chroma>
  <annotation>
  Hadron spectrum input
  </annotation>
  <Param>
    <InlineMeasurements>
EOF

## ======================================================= ##
## ====================== MAKE SOURCE ==================== ##
## ======================================================= ##

print <<"EOF";
      <elem>
        <Name>MAKE_SOURCE</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>6</version>
          <Source>
            <version>2</version>
            <SourceType>SHELL_SOURCE</SourceType>
            <j_decay>3</j_decay>
            <t_srce>0 0 0 0</t_srce>
            <SmearingParam>
              <wvf_kind>GAUGE_INV_GAUSSIAN</wvf_kind>
              <wvf_param>2.0</wvf_param>
              <wvfIntPar>5</wvfIntPar>
              <no_smear_dir>3</no_smear_dir>
            </SmearingParam>
            <LinkSmearing>
              <LinkSmearingType>APE_SMEAR</LinkSmearingType>
              <link_smear_fact>2.5</link_smear_fact>
              <link_smear_num>1</link_smear_num>
              <no_smear_dir>3</no_smear_dir>
            </LinkSmearing>
          </Source>
        </Param>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
          <source_id>sh_source_1</source_id>
        </NamedObject>
      </elem>
EOF

## ======================================================= ##
## ====================== PROPAGATOR ===================== ##
## ======================================================= ##

print <<"EOF";
      <elem>
        <Name>PROPAGATOR</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>10</version>
          <quarkSpinType>FULL</quarkSpinType>
          <obsvP>false</obsvP>
          <numRetries>1</numRetries>
          <FermionAction>
            <FermAct>WILSON</FermAct>
            <Kappa>0.11</Kappa>
            <AnisoParam>
              <anisoP>false</anisoP>
              <t_dir>3</t_dir>
              <xi_0>1.0</xi_0>
              <nu>1.0</nu>
            </AnisoParam>
            <FermionBC>
              <FermBC>SIMPLE_FERMBC</FermBC>
              <boundary>1 1 1 -1</boundary>
            </FermionBC>
          </FermionAction>
          <InvertParam>
            <invType>CG_INVERTER</invType>
            <RsdCG>1.0e-12</RsdCG>
            <MaxCG>1000</MaxCG>
          </InvertParam>
        </Param>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
          <source_id>sh_source_1</source_id>
          <prop_id>sh_prop_1</prop_id>
        </NamedObject>
      </elem>
EOF

## ======================================================= ##
## ====================== SINK SMEAR ===================== ##
## ======================================================= ##

print <<"EOF";
      <elem>
        <Name>SINK_SMEAR</Name>
        <Frequency>1</Frequency>
        <Param>
          <version>5</version>
          <Sink>
            <version>2</version>
            <SinkType>POINT_SINK</SinkType>
            <j_decay>3</j_decay>
            <Displacement>
              <version>1</version>
              <DisplacementType>NONE</DisplacementType>
            </Displacement>
            <LinkSmearing>
              <LinkSmearingType>APE_SMEAR</LinkSmearingType>
              <link_smear_fact>2.5</link_smear_fact>
              <link_smear_num>1</link_smear_num>
              <no_smear_dir>3</no_smear_dir>
            </LinkSmearing>
          </Sink>
        </Param>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
          <prop_id>sh_prop_1</prop_id>
          <smeared_prop_id>sh_pt_sink_1</smeared_prop_id>
        </NamedObject>
      </elem>
EOF


## ======================================================= ##
## ==================== HADRON CONTRACT ================== ##
## ======================================================= ##

print <<"EOF";
      <elem>
        <Name>HADRON_CONTRACT</Name>
        <Frequency>1</Frequency>
        <NamedObject>
          <gauge_id>default_gauge_field</gauge_id>
          <output_file>${output_file}</output_file>
          <Contractions>
            <elem>
              <version>1</version>
              <ContractionType>diagonal_gamma_mesons</ContractionType>
              <mom2_max>0</mom2_max>
              <!-- zero momentum -->
              <avg_equiv_mom>true</avg_equiv_mom>
              <mom_origin>0 0 0</mom_origin>
              <first_id>sh_pt_sink_1</first_id>
              <second_id>sh_pt_sink_1</second_id>
            </elem>
          </Contractions>
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
  <RNG>
    <Seed>
      <elem>11</elem>
      <elem>11</elem>
      <elem>11</elem>
      <elem>0</elem>
    </Seed>
  </RNG>
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