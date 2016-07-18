;; Auto-generated. Do not edit!


(when (boundp 'roscompat::Num)
  (if (not (find-package "ROSCOMPAT"))
    (make-package "ROSCOMPAT"))
  (shadow 'Num (find-package "ROSCOMPAT")))
(unless (find-package "ROSCOMPAT::NUM")
  (make-package "ROSCOMPAT::NUM"))

(in-package "ROS")
;;//! \htmlinclude Num.msg.html


(defclass roscompat::Num
  :super ros::object
  :slots (_num _numArr ))

(defmethod roscompat::Num
  (:init
   (&key
    ((:num __num) 0)
    ((:numArr __numArr) (make-array 0 :initial-element 0 :element-type :integer))
    )
   (send-super :init)
   (setq _num (round __num))
   (setq _numArr __numArr)
   self)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:numArr
   (&optional __numArr)
   (if __numArr (setq _numArr __numArr)) _numArr)
  (:serialization-length
   ()
   (+
    ;; int64 _num
    8
    ;; int64[] _numArr
    (* 8    (length _numArr)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int64 _num
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _num (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _num) (= (length (_num . bv)) 2)) ;; bignum
              (write-long (ash (elt (_num . bv) 0) 0) s)
              (write-long (ash (elt (_num . bv) 1) -1) s))
             ((and (class _num) (= (length (_num . bv)) 1)) ;; big1
              (write-long (elt (_num . bv) 0) s)
              (write-long (if (>= _num 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _num s)(write-long (if (>= _num 0) 0 #xffffffff) s)))
     ;; int64[] _numArr
     (write-long (length _numArr) s)
     (dotimes (i (length _numArr))
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke (elt _numArr i) (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class (elt _numArr i)) (= (length ((elt _numArr i) . bv)) 2)) ;; bignum
              (write-long (ash (elt ((elt _numArr i) . bv) 0) 0) s)
              (write-long (ash (elt ((elt _numArr i) . bv) 1) -1) s))
             ((and (class (elt _numArr i)) (= (length ((elt _numArr i) . bv)) 1)) ;; big1
              (write-long (elt ((elt _numArr i) . bv) 0) s)
              (write-long (if (>= (elt _numArr i) 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long (elt _numArr i) s)(write-long (if (>= (elt _numArr i) 0) 0 #xffffffff) s)))
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int64 _num
#+(or :alpha :irix6 :x86_64)
      (setf _num (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _num (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64[] _numArr
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _numArr (instantiate integer-vector n))
     (dotimes (i n)
#+(or :alpha :irix6 :x86_64)
      (setf (elt _numArr i) (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf (elt _numArr i) (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
     ))
   ;;
   self)
  )

(setf (get roscompat::Num :md5sum-) "929263e3d4dc7a52f6a6c02159310be0")
(setf (get roscompat::Num :datatype-) "roscompat/Num")
(setf (get roscompat::Num :definition-)
      "int64 num
int64[] numArr

")



(provide :roscompat/Num "929263e3d4dc7a52f6a6c02159310be0")


