TITLE Cerebellum Basket Cell Model

COMMENT
	adapted from: 
	"Cerebellum Golgi Cell Model
        Na transient channel
	Gutfreund parametrization
   
	Author: E.DAngelo, T.Nieus, A. Fontana
	Last revised: 8.5.2000"
	
	to match Na dynamics as in net_hh_w.mod by I. Vida, Nov 2000	
	adapted by: Birgit Kriener
	Last revised: 13.2.2017
ENDCOMMENT
 
NEURON { 
	SUFFIX Na_BC
	NONSPECIFIC_CURRENT ina
	RANGE gmax, g, egna
	RANGE alpha_m, beta_m, alpha_h, beta_h 
	RANGE Aalpha_m, Kalpha_m, V0alpha_m
	RANGE Abeta_m, Kbeta_m, V0beta_m
	RANGE Aalpha_h, Kalpha_h, V0alpha_h
	RANGE Abeta_h, Kbeta_h, V0beta_h
	RANGE m, h, m_inf, h_inf, tau_h, tcorr
} 
 
UNITS { 
	(mA) = (milliamp) 
	(mV) = (millivolt) 
} 
 
PARAMETER { 
	egna     = 55. (mV)
	
	Aalpha_m = 0.1 (/ms-mV)
	Kalpha_m = -10. (mV)
	V0alpha_m = -35. (mV)
	
	Abeta_m = 4. (/ms)
	Kbeta_m = -18. (mV)
	V0beta_m = -60. (mV)

	Aalpha_h  = 0.35 (/ms)
	Kalpha_h  = -20. (mV)
	V0alpha_h = -58. (mV)
 
	Abeta_h  = 5. (/ms)
	Kbeta_h  = -10. (mV)
	V0beta_h = -28. (mV)
	 
	gmax = 0.035 (mho/cm2) 	  
	v (mV) 
	celsius (degC)
	Q10 = 3 (1)
} 

STATE { 
	m 
	h 
} 

ASSIGNED { 
	ina (mA/cm2) 
	m_inf 
	h_inf 
	tau_h (ms) 
	g (mho/cm2) 
	alpha_m (/ms)
	beta_m (/ms)
	alpha_h (/ms)
	beta_h (/ms)
	tcorr	(1)
} 
 
INITIAL { 
	rate(v) 
	m = m_inf 
	h = h_inf 
} 
 
BREAKPOINT { 
	SOLVE states METHOD cnexp 
	m = m_inf
	g = gmax*m*m*m*h 
	ina = g*(v - egna)
	alpha_m = alp_m(v)
	beta_m = bet_m(v) 
	alpha_h = alp_h(v)
	beta_h = bet_h(v) 
} 
 
DERIVATIVE states { 
	rate(v) 
	h' =(h_inf - h)/tau_h 
} 
 
FUNCTION alp_m(v(mV))(/ms) {
	alp_m = Aalpha_m*linoid(v-V0alpha_m,Kalpha_m) 
} 
 
FUNCTION bet_m(v(mV))(/ms) {
	bet_m = Abeta_m*exp((v-V0beta_m)/Kbeta_m) 
} 
 
FUNCTION alp_h(v(mV))(/ms) {
	tcorr = Q10^((celsius-6.3(degC))/10(degC)) 
	alp_h = tcorr*Aalpha_h*exp((v-V0alpha_h)/Kalpha_h) 
} 
 
FUNCTION bet_h(v(mV))(/ms) {
	tcorr = Q10^((celsius-6.3(degC))/10(degC)) 
	bet_h = tcorr*Abeta_h/(1+exp((v-V0beta_h)/Kbeta_h))
} 
 
PROCEDURE rate(v (mV)) {LOCAL a_m, b_m, a_h, b_h 
	TABLE m_inf, h_inf, tau_h 
	DEPEND Aalpha_m, Kalpha_m, V0alpha_m, 
	       Abeta_m, Kbeta_m, V0beta_m,
               Aalpha_h, Kalpha_h, V0alpha_h,
               Abeta_h, Kbeta_h, V0beta_h, celsius FROM -100 TO 100 WITH 200 
		
	a_m = alp_m(v)  
	b_m = bet_m(v) 
	a_h = alp_h(v)  
	b_h = bet_h(v) 
	m_inf = a_m/(a_m + b_m) 
	h_inf = a_h/(a_h + b_h) 
	tau_h = 1/(a_h + b_h)
	
} 

FUNCTION linoid(x (mV),y (mV)) (mV) {
        if (fabs(x/y) < 1e-6) {
                linoid = y*(1 - x/y/2)
        }else{
                linoid = x/(1 - exp(x/y))
        }
}

