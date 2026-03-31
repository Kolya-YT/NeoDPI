# Keep JNI methods
-keepclasseswithmembernames class * {
    native <methods>;
}

-keep class com.neodpi.app.core.ByeDpiProxy { *; }

-keep,allowoptimization class com.neodpi.app.core.TProxyService { *; }
-keep,allowoptimization class com.neodpi.app.activities.** { *; }
-keep,allowoptimization class com.neodpi.app.services.** { *; }
-keep,allowoptimization class com.neodpi.app.receiver.** { *; }

-keep class com.neodpi.app.fragments.** {
    <init>();
}

-keep,allowoptimization class com.neodpi.app.data.** {
    <fields>;
}

-keepattributes Signature
-keepattributes *Annotation*

-repackageclasses 'com.neodpi'
-renamesourcefileattribute ''
-keepattributes SourceFile,InnerClasses,EnclosingMethod,Signature,RuntimeVisibleAnnotations,*Annotation*,*Parcelable*
-allowaccessmodification
-overloadaggressively
-optimizationpasses 5
-verbose
-dontusemixedcaseclassnames
-adaptclassstrings
-adaptresourcefilecontents **.xml,**.json
-adaptresourcefilenames **.xml,**.json