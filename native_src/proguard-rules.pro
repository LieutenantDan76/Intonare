# ============================================================================
#  Intonare release rules for R8 (code shrinking and name scrambling).
#  Master copy: native_src\proguard-rules.pro. go.bat copies it to
#  android\app\proguard-rules.pro on every run.
#
#  Why so few rules: Capacitor core and each plugin already ship their own
#  "consumer" rules inside their libraries. The Android default file
#  (proguard-android-optimize.txt) already keeps @JavascriptInterface methods
#  and the annotation attributes. The rules below cover what is ours, plus
#  explicit copies of the upstream rules, so an upstream change cannot break
#  the app without a sound.
# ============================================================================

# --- 1. Crash reports -------------------------------------------------------
# Keep line numbers so Play Console can show readable stack traces. The AAB
# carries the mapping file, so Play un-scrambles the names by itself.
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Capacitor reads annotations at run time (@CapacitorPlugin, @PluginMethod,
# @ActivityCallback). Same as the Android default file, listed here on purpose.
-keepattributes RuntimeVisibleAnnotations,RuntimeVisibleParameterAnnotations,AnnotationDefault,Signature,InnerClasses,EnclosingMethod

# --- 2. Our three native Capacitor plugins ----------------------------------
# JS finds a plugin by class name and calls its @PluginMethod methods by name.
# If R8 renames either one, JS reports "plugin is not implemented on android".
-keep public class com.lieutenantdan.intonare.IntonareMicPlugin { *; }
-keep public class com.lieutenantdan.intonare.IntonareHapticsPlugin { *; }
-keep public class com.lieutenantdan.intonare.FileSaverPlugin { *; }

# --- 3. The IntonareNative bridge in MainActivity ---------------------------
# The page calls window.IntonareNative.setSplashSound(), getTopInset() and
# playSplashSound() by name.
-keepclassmembers class com.lieutenantdan.intonare.MainActivity$SplashSoundBridge {
    @android.webkit.JavascriptInterface <methods>;
}

# --- 4. Plugin classes that Capacitor loads by name -------------------------
# capacitor.plugins.json lists each plugin by full class name and Capacitor
# loads it with Class.forName. Copy of the Capacitor core consumer rule:
-keep public class * extends com.getcapacitor.Plugin { *; }
# The plugin glue packages are small. Keeping them whole costs almost nothing:
#   App, Filesystem, Haptics, Local Notifications, Screen Orientation, Share,
#   Status Bar
-keep class com.capacitorjs.plugins.** { *; }
#   App Update (capawesome)
-keep class io.capawesome.capacitorjs.plugins.appupdate.** { *; }
#   RevenueCat Capacitor plugin (the RevenueCat SDK ships its own rules)
-keep class com.revenuecat.purchases.capacitor.** { *; }
