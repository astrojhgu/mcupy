#include <boost/ref.hpp>
#include <boost/utility.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/module.hpp>
#include <boost/python/class.hpp>
#include <boost/python/operators.hpp>
#include <boost/python/def.hpp>
#include <boost/python/pure_virtual.hpp>
#include <boost/python/copy_const_reference.hpp>
#include <boost/python/call.hpp>
#include <boost/operators.hpp>
#include <boost/python/overloads.hpp>
#include <vector>
#include <fstream>

#define private public
#include <core/node.hpp>
#include <core/stochastic_node.hpp>
#include <core/deterministic_node.hpp>
#include <core/differentiable_dtm_node.hpp>
#include <core/tag_t.hpp>
#include <core/wrappered_graph.hpp>
#include <core/urand.hpp>

#include <core/mixture_node.hpp>
#include <tools/dump_graph_topology.hpp>

#include<nodes/abs_node.hpp>
#include<nodes/bern_node.hpp>
#include<nodes/beta_node.hpp>
#include<nodes/bin_node.hpp>
#include<nodes/bvnormal_node.hpp>
#include<nodes/cauchy_node.hpp>
#include<nodes/chisqr_node.hpp>
#include<nodes/const_node.hpp>
#include<nodes/cond_node.hpp>
#include<nodes/cos_node.hpp>
#include<nodes/dexp_node.hpp>
#include<nodes/exp_node.hpp>
#include<nodes/exp_dist_node.hpp>
#include<nodes/f_node.hpp>
#include<nodes/gamma_node.hpp>
#include<nodes/gen_gamma_node.hpp>
#include<nodes/ilogit_node.hpp>
#include<nodes/log10_node.hpp>
#include<nodes/logit_node.hpp>
#include<nodes/log_node.hpp>
#include<nodes/logistic_node.hpp>
#include<nodes/log_normal_node.hpp>
#include<nodes/normal_node.hpp>
#include<nodes/pareto_node.hpp>
#include<nodes/phi_node.hpp>
#include<nodes/poisson_node.hpp>
#include<nodes/str_node.hpp>
#include<nodes/sin_node.hpp>
#include<nodes/sqrt_node.hpp>
#include<nodes/step_node.hpp>
#include<nodes/tan_node.hpp>
#include<nodes/t_node.hpp>
#include<nodes/trunc_pareto_node.hpp>
#include<nodes/uniform_node.hpp>
#include<nodes/discrete_uniform_node.hpp>
#include<nodes/arithmetic_node.hpp>
#include<nodes/compare_node.hpp>
#include<nodes/switch_node.hpp>

using namespace boost::python;
using namespace boost;
using namespace mcmc_utilities;

class node_wrap
  :public node<double,std_vector>,
   public wrapper<node<double,std_vector> >
{
private:
  double do_value(size_t idx)const
  {
    return this->get_override("do_value")();
  }

  void do_connect_to_parent(node<double,std_vector>* prhs,size_t n,size_t idx)
  {
    this->get_override("do_connect_to_parent")(prhs,n,idx);
  }

  void do_init_value(size_t n)
  {
    if(override f=this->get_override("do_init_value"))
      {
	f();
      }
    return node<double,std_vector>::do_init_value(n);
  }

  void default_do_init_value(size_t n)
  {
    return this->node<double,std_vector>::do_init_value(n);
  }

public:
  node_wrap(size_t nparents,size_t ndim1)
    :node(nparents,ndim1)
  {}
};


class stochastic_node_wrap
  :public stochastic_node<double,std_vector>,
   public wrapper<stochastic_node<double,std_vector> >
{
  double do_log_prob()const
  {
    return this->get_override("do_log_prob")();
  }

  bool is_continuous(size_t idx)const
  {
    return this->get_override("is_continuous")(idx);
  }

  std::pair<double,double> do_var_range()const
  {
    return this->get_override("do_var_range")();
  }

  std::vector<double> do_candidate_points()const
  {
    if(override f=this->get_override("do_candidate_points"))
      {
	return f();
      }
    return this->stochastic_node<double,std_vector>::do_candidate_points();
  }

  std::vector<double> do_init_points()const
  {
    if(override f=this->get_override("do_init_points"))
      {
	return f();
      }
    return this->stochastic_node<double,std_vector>::do_init_points();
  }

public:
  stochastic_node_wrap(size_t np,const std::vector<double>& v)
    :stochastic_node<double,std_vector>(np,v)
  {}

  stochastic_node_wrap(size_t np,double v)
    :stochastic_node<double,std_vector>(np,v)
  {}
};


class deterministic_node_wrap
  :public deterministic_node<double,std_vector>,
   public wrapper<deterministic_node<double,std_vector> >
{
private:  
  double do_calc(size_t idx,const std::vector<double>& parents)const
  {
    return this->get_override("do_calc")(idx,parents);
  }
public:
  deterministic_node_wrap(size_t nparents,size_t ndim)
    :deterministic_node<double,std_vector>(nparents,ndim)
  {}
};

class differentiable_dtm_node_wrap
  :public differentiable_dtm_node<double,std_vector>,
   public wrapper<differentiable_dtm_node<double,std_vector> >
{
public:
  double do_calc(size_t idx,const std::vector<double>& parents)const
  {
    return this->get_override("do_calc")(idx,parents);
  }

public:
  differentiable_dtm_node_wrap(size_t nparents,size_t ndim)
    :differentiable_dtm_node<double,std_vector>(nparents,ndim)
  {
  }
};


template <typename Tnode,typename ...Args>
std::shared_ptr<node<double,std_vector> > create_node(Args ...args)
{
  return std::shared_ptr<node<double,std_vector> >(new Tnode(args...));
}


template <typename T>
bool test_node_kind(const std::shared_ptr<node<double,std_vector> >& p)
{
  return bool(dynamic_pointer_cast<T>(p));
}

template <typename T>
std::shared_ptr<T> cast_to(const std::shared_ptr<node<double,std_vector> >& p)
{
  auto result=dynamic_pointer_cast<T>(p);
  if (!bool(result))
    {
      throw std::runtime_error("cannot be convert to subclass");
    }
  return result;
}

int num_of_parents(const std::shared_ptr<node<double,std_vector> >& p)
{
  return p->num_of_parents();
}

int num_of_dims(const std::shared_ptr<node<double,std_vector> >& p)
{
  return p->num_of_dims();
}

void set_value(std::shared_ptr<node<double,std_vector> >& p,int idx,double v)
{
  auto p_stochastic=dynamic_pointer_cast<mcmc_utilities::stochastic_node<double,std_vector> >(p);
  if(p_stochastic)
    {
      p_stochastic->set_value(idx,v);
    }
}

void set_observed(std::shared_ptr<node<double,std_vector> >& p,int idx,bool o)
{
  auto p_stochastic=dynamic_pointer_cast<mcmc_utilities::stochastic_node<double,std_vector> >(p);
  if(p_stochastic)
    {
      p_stochastic->set_observed(idx,o);
    }
}

double pyarms(PyObject* func,double x1,double x2,double xcur)
{
  static urand<double> rnd;
  auto pd=[func](double x)->double {return boost::python::call<double> (func,x);};
  size_t xmc=0;
  return arms(pd,std::pair<double,double>(x1,x2),xcur,10,rnd,xmc);
}

double eval_expr(const std::string& expr,const std::vector<std::string>& args,const std::vector<double>& params)
{
  return str_node<double,std_vector>::eval_expr(expr,args,params);
}


BOOST_PYTHON_MODULE(core)
{
  
  def("arms",&pyarms);
  
  class_<std::weak_ptr<node<double,std_vector> > >("weak_node_ptr");
  
  class_<std::vector<double> >("vector",boost::python::init<size_t>())
    .def(vector_indexing_suite<std::vector<double> >())
    .def("append",(void (std::vector<double>::*)(const double&))&std::vector<double>::push_back);

  class_<std::vector<std::string> >("str_vec",boost::python::init<size_t>())
    .def(vector_indexing_suite<std::vector<std::string> >())
    .def("append",(void (std::vector<std::string>::*)(const std::string&))&std::vector<std::string>::push_back);

  class_<std::vector<std::pair<mcmc_utilities::tag_t,size_t> > >("tag_vec")
	 .def(vector_indexing_suite<std::vector<std::pair<mcmc_utilities::tag_t,size_t> > >());

  class_<std::vector<std::shared_ptr<mcmc_utilities::node<double,std_vector> > > >("node_vec")
    .def(vector_indexing_suite<std::vector<std::shared_ptr<mcmc_utilities::node<double,std_vector> > > >())
    .def("append",(void (std::vector<std::shared_ptr<mcmc_utilities::node<double,std_vector> > >::*)(const std::shared_ptr<mcmc_utilities::node<double,std_vector> > &))&std::vector<std::shared_ptr<mcmc_utilities::node<double,std_vector> > >::push_back);

  class_<std::vector<std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > > >("stochastic_node_vec")
    .def(vector_indexing_suite<std::vector<std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > > >())
    .def("append",(void (std::vector<std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > >::*)(const std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > &))&std::vector<std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > >::push_back);

  class_<std::pair<mcmc_utilities::tag_t,size_t> >("tag_pair",
						   boost::python::init<mcmc_utilities::tag_t,size_t>());


  class_<std::shared_ptr<mcmc_utilities::node<double,std_vector> > >("node_ptr",boost::python::init<>());
  class_<std::shared_ptr<mcmc_utilities::stochastic_node<double,std_vector> > >("stochastic_node_ptr",boost::python::init<>());
  //def("pair",&std::make_pair<mcmc_utilities::tag_t,size_t>);
  
  class_<node_wrap, noncopyable>("node",boost::python::init<size_t,size_t>())
    .def("value",&node<double,std_vector>::value)
    .def("do_value",pure_virtual(&node<double,std_vector>::do_value))
    .def("do_init_value",pure_virtual(&node<double,std_vector>::do_init_value))
    .def("init_value",(void (node<double,std_vector>::*)())&node<double,std_vector>::init_value)
    .def("init_valueialize1",(void (node<double,std_vector>::*)(size_t))&node<double,std_vector>::init_value)
    ;

  class_<stochastic_node_wrap,noncopyable,bases<node<double,std_vector> > >("stochastic_node",boost::python::init<size_t,const std::vector<double>&>())
    .def(boost::python::init<size_t,double>())
    .def("do_log_prob",pure_virtual(&stochastic_node<double,std_vector>::do_log_prob))
    .def("do_var_range",pure_virtual(&stochastic_node<double,std_vector>::do_var_range))
    .def("do_init_points",pure_virtual(&stochastic_node<double,std_vector>::do_init_points))
    ;
    

  class_<deterministic_node_wrap,bases<node<double,std_vector> > ,noncopyable>("deterministic_node",
									       boost::python::init<size_t,size_t>())
    .def("do_calc",pure_virtual(&deterministic_node<double,std_vector>::do_calc))
    ;

  class_<differentiable_dtm_node_wrap,bases<deterministic_node<double,std_vector> > ,noncopyable>("differentiable_dtm_node",
											    boost::python::init<size_t,size_t>())
    ;

  
  class_<mcmc_utilities::tag_t>("tag_t",boost::python::init<std::string,int>())
    .def(boost::python::init<std::string>())
    .def(boost::python::init<std::string,int,bool>())
    .def("name",&mcmc_utilities::tag_t::name)
    .def("idx",&mcmc_utilities::tag_t::idx)
    .def("is_array",&mcmc_utilities::tag_t::is_array)
    .def(str(self))
    ;

  
  class_<monitor_type<double> >("monitor_type",boost::python::init<const std::function<double()> >())
    .def("get",&monitor_type<double>::get)
    ;

  node_adder<double,mcmc_utilities::tag_t> (wrappered_graph<double,mcmc_utilities::tag_t>::*add_node1)(std::shared_ptr<mcmc_utilities::node<double,std_vector> >&,const mcmc_utilities::tag_t& t)=&wrappered_graph<double,mcmc_utilities::tag_t>::add_node;
  
  class_<wrappered_graph<double,mcmc_utilities::tag_t>,noncopyable>("cppgraph",boost::python::init<>())
    .def("sample",&wrappered_graph<double,mcmc_utilities::tag_t>::sample)
    .def("get_monitor",&wrappered_graph<double,mcmc_utilities::tag_t>::get_monitor)
    .def("set_value",&wrappered_graph<double,mcmc_utilities::tag_t>::set_value)
    .def("get_value",&wrappered_graph<double,mcmc_utilities::tag_t>::get_value)
    .def("is_observed",&wrappered_graph<double,mcmc_utilities::tag_t>::is_observed)
    .def("set_observed",&wrappered_graph<double,mcmc_utilities::tag_t>::set_observed)
    .def("add_node",add_node1)
    ;

  
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_parent1)(const std::pair<mcmc_utilities::tag_t,size_t>&)=&node_adder<double,mcmc_utilities::tag_t>::with_parent;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_parent2)(const mcmc_utilities::tag_t&,size_t)=&node_adder<double,mcmc_utilities::tag_t>::with_parent;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_parent3)(const mcmc_utilities::tag_t&)=&node_adder<double,mcmc_utilities::tag_t>::with_parent;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_parent4)(const std::shared_ptr<node<double,std_vector> >& ,size_t)=&node_adder<double,mcmc_utilities::tag_t>::with_parent;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_parent5)(const std::shared_ptr<node<double,std_vector> >&)=&node_adder<double,mcmc_utilities::tag_t>::with_parent;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_value1)(const double&)=&node_adder<double,mcmc_utilities::tag_t>::with_value;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_value2)(const std_vector<double>&)=&node_adder<double,mcmc_utilities::tag_t>::with_value;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_value3)(size_t,const double&)=&node_adder<double,mcmc_utilities::tag_t>::with_value;

  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_observed_value1)(const double&)=&node_adder<double,mcmc_utilities::tag_t>::with_observed_value;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_observed_value2)(const std_vector<double>&)=&node_adder<double,mcmc_utilities::tag_t>::with_observed_value;
  node_adder<double,mcmc_utilities::tag_t>& (node_adder<double,mcmc_utilities::tag_t>::*with_observed_value3)(size_t,const double&)=&node_adder<double,mcmc_utilities::tag_t>::with_observed_value;
  
  
  class_<node_adder<double,mcmc_utilities::tag_t>>("node_adder",boost::python::init<wrappered_graph<double,mcmc_utilities::tag_t>&,std::shared_ptr<mcmc_utilities::node<double,std_vector> >,const mcmc_utilities::tag_t&>())
    .def("with_parent",with_parent1,return_value_policy<return_by_value>())
    .def("with_parent",with_parent2,return_value_policy<return_by_value>())
    .def("with_parent",with_parent3,return_value_policy<return_by_value>())
    .def("with_parent",with_parent4,return_value_policy<return_by_value>())
    .def("with_parent",with_parent5,return_value_policy<return_by_value>())
    .def("with_value",with_value1,return_value_policy<return_by_value>())
    .def("with_value",with_value2,return_value_policy<return_by_value>())
    .def("with_value",with_value3,return_value_policy<return_by_value>())
    .def("with_observed_value",with_observed_value1,return_value_policy<return_by_value>())
    .def("with_observed_value",with_observed_value2,return_value_policy<return_by_value>())
    .def("with_observed_value",with_observed_value3,return_value_policy<return_by_value>())
    .def("done",&node_adder<double,mcmc_utilities::tag_t>::done)
    .def("with_tag",&node_adder<double,mcmc_utilities::tag_t>::with_tag,return_value_policy<return_by_value>())
    ;


  
  def("eval_expr",&eval_expr);
  
  def("abs_node",&create_node<abs_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("bern_node",&create_node<bern_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("beta_node",&create_node<beta_node<double,std_vector>,double,double>,return_value_policy<return_by_value>());
  def("bin_node",&create_node<bin_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("bvnormal_node",&create_node<bvnormal_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("cauchy_node",&create_node<cauchy_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("chisqr_node",&create_node<chisqr_node<double,std_vector>, int>,return_value_policy<return_by_value>());
  def("const_node",&create_node<const_node<double,std_vector>,double >,return_value_policy<return_by_value>());
  def("cos_node",&create_node<cos_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("dexp_node",&create_node<dexp_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("exp_node",&create_node<exp_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("exp_dist_node",&create_node<exp_dist_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("f_node",&create_node<f_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("gamma_node",&create_node<gamma_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("gen_gamma_node",&create_node<gen_gamma_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("ilogit_node",&create_node<ilogit_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("log10_node",&create_node<log10_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("logit_node",&create_node<logit_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("logistic_node",&create_node<logistic_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("log_node",&create_node<log_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("log_normal_node",&create_node<log_normal_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("normal_node",&create_node<normal_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("pareto_node",&create_node<pareto_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("phi_node",&create_node<phi_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("poisson_node",&create_node<poisson_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("sin_node",&create_node<sin_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("sqrt_node",&create_node<sqrt_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("step_node",&create_node<step_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("tan_node",&create_node<tan_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("t_node",&create_node<t_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("trunc_pareto_node",&create_node<trunc_pareto_node<double,std_vector>,double>,return_value_policy<return_by_value>());
  def("fixed_uniform_node",&create_node<fixed_uniform_node<double,std_vector>,double,double>,return_value_policy<return_by_value>());
  def("uniform_node",&create_node<uniform_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("discrete_uniform_node",&create_node<discrete_uniform_node<double,std_vector>,int,int>,return_value_policy<return_by_value>());
  def("str_node_",&create_node<str_node<double,std_vector>,const std::string&,const std::vector<std::string>&>,return_value_policy<return_by_value>());

  def("add_node",&create_node<add_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("sub_node",&create_node<sub_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("mul_node",&create_node<mul_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("div_node",&create_node<div_node<double,std_vector> >,return_value_policy<return_by_value>());
  
  def("lt_node",&create_node<lt_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("le_node",&create_node<le_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("gt_node",&create_node<gt_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("ge_node",&create_node<ge_node<double,std_vector> >,return_value_policy<return_by_value>());
  def("eq_node",&create_node<eq_node<double,std_vector> >,return_value_policy<return_by_value>());
  
  def("switch_node",&create_node<switch_node<double,std_vector>,int >,return_value_policy<return_by_value>());

  def("cond_node",&create_node<cond_node<double,std_vector> >,return_value_policy<return_by_value>());

  def("mixture_node",&create_node<mixture_node<double,std_vector>,const std::vector<std::shared_ptr<stochastic_node<double,std_vector> > >& >,return_value_policy<return_by_value>());
  
  def("is_deterministic_node",&test_node_kind<deterministic_node<double,std_vector> >);
  def("is_stochastic_node",&test_node_kind<stochastic_node<double,std_vector> >);
  def("nparents",&num_of_parents);
  def("ndims",&num_of_dims);
  def("set_value",&set_value);
  def("set_observed",&set_observed);

  def("convert_to_stochastic",&cast_to<stochastic_node<double,std_vector> >);

}
