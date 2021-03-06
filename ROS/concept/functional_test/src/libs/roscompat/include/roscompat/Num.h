// Generated by gencpp from file roscompat/Num.msg
// DO NOT EDIT!


#ifndef ROSCOMPAT_MESSAGE_NUM_H
#define ROSCOMPAT_MESSAGE_NUM_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace roscompat
{
template <class ContainerAllocator>
struct Num_
{
  typedef Num_<ContainerAllocator> Type;

  Num_()
    : num(0)
    , numArr()  {
    }
  Num_(const ContainerAllocator& _alloc)
    : num(0)
    , numArr(_alloc)  {
    }



   typedef int64_t _num_type;
  _num_type num;

   typedef std::vector<int64_t, typename ContainerAllocator::template rebind<int64_t>::other >  _numArr_type;
  _numArr_type numArr;




  typedef boost::shared_ptr< ::roscompat::Num_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::roscompat::Num_<ContainerAllocator> const> ConstPtr;

}; // struct Num_

typedef ::roscompat::Num_<std::allocator<void> > Num;

typedef boost::shared_ptr< ::roscompat::Num > NumPtr;
typedef boost::shared_ptr< ::roscompat::Num const> NumConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::roscompat::Num_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::roscompat::Num_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace roscompat

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/jade/share/std_msgs/cmake/../msg'], 'roscompat': ['/home/fran/git/testRos/src/libs/roscompat/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::roscompat::Num_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::roscompat::Num_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::roscompat::Num_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::roscompat::Num_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::roscompat::Num_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::roscompat::Num_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::roscompat::Num_<ContainerAllocator> >
{
  static const char* value()
  {
    return "929263e3d4dc7a52f6a6c02159310be0";
  }

  static const char* value(const ::roscompat::Num_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x929263e3d4dc7a52ULL;
  static const uint64_t static_value2 = 0xf6a6c02159310be0ULL;
};

template<class ContainerAllocator>
struct DataType< ::roscompat::Num_<ContainerAllocator> >
{
  static const char* value()
  {
    return "roscompat/Num";
  }

  static const char* value(const ::roscompat::Num_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::roscompat::Num_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 num\n\
int64[] numArr\n\
";
  }

  static const char* value(const ::roscompat::Num_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::roscompat::Num_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.num);
      stream.next(m.numArr);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct Num_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::roscompat::Num_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::roscompat::Num_<ContainerAllocator>& v)
  {
    s << indent << "num: ";
    Printer<int64_t>::stream(s, indent + "  ", v.num);
    s << indent << "numArr[]" << std::endl;
    for (size_t i = 0; i < v.numArr.size(); ++i)
    {
      s << indent << "  numArr[" << i << "]: ";
      Printer<int64_t>::stream(s, indent + "  ", v.numArr[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROSCOMPAT_MESSAGE_NUM_H
