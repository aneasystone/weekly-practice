#include "jni.h"
#include "JNIDemo.h"
#include <stdio.h>

JNIEXPORT void JNICALL Java_JNIDemo_sayHello(JNIEnv *env, jobject jobj) {
    printf("Hello World!\n");
}

/**
 * gcc -I${JAVA_HOME}/include -I${JAVA_HOME}/include/darwin -dynamiclib JNIDemo.c -o libJNIDemo.dylib
 */