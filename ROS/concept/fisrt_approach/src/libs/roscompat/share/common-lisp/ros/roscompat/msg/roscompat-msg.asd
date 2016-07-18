
(cl:in-package :asdf)

(defsystem "roscompat-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Num" :depends-on ("_package_Num"))
    (:file "_package_Num" :depends-on ("_package"))
    (:file "Pose3d" :depends-on ("_package_Pose3d"))
    (:file "_package_Pose3d" :depends-on ("_package"))
  ))