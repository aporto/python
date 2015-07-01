       //turns off console messages - default is to print messages
        static void setVerbose(bool _verbose);

        //Functions in rough order they should be used.
        static int listDevices(bool silent = false);

        //needs to be called after listDevices - otherwise returns NULL
        static char * getDeviceName(int deviceID);

        //choose to use callback based capture - or single threaded
        void setUseCallback(bool useCallback);

        //call before setupDevice
        //directshow will try and get the closest possible framerate to what is requested
        void setIdealFramerate(int deviceID, int idealFramerate);

        //some devices will stop delivering frames after a while - this method gives you the option to try and reconnect
        //to a device if videoInput detects that a device has stopped delivering frames.
        //you MUST CALL isFrameNew every app loop for this to have any effect
        void setAutoReconnectOnFreeze(int deviceNumber, bool doReconnect, int numMissedFramesBeforeReconnect);

        //Choose one of these five to setup your device
        bool setupDevice(int deviceID);
        bool setupDevice(int deviceID, int w, int h);
        bool setupDeviceFourcc(int deviceID, int w, int h,int fourcc);

        //These two are only for capture cards
        //USB and Firewire cameras souldn't specify connection
        bool setupDevice(int deviceID, int connection);
        bool setupDevice(int deviceID, int w, int h, int connection);

        bool setFourcc(int deviceNumber, int fourcc);

        //If you need to you can set your NTSC/PAL/SECAM
        //preference here. if it is available it will be used.
        //see #defines above for available formats - eg VI_NTSC_M or VI_PAL_B
        //should be called after setupDevice
        //can be called multiple times
        bool setFormat(int deviceNumber, int format);

        //Tells you when a new frame has arrived - you should call this if you have specified setAutoReconnectOnFreeze to true
        bool isFrameNew(int deviceID);

        bool isDeviceSetup(int deviceID);

        //Returns the pixels - flipRedAndBlue toggles RGB/BGR flipping - and you can flip the image too
        unsigned char * getPixels(int deviceID, bool flipRedAndBlue = true, bool flipImage = false);

        //Or pass in a buffer for getPixels to fill returns true if successful.
        bool getPixels(int id, unsigned char * pixels, bool flipRedAndBlue = true, bool flipImage = false);

        //Launches a pop up settings window
        //For some reason in GLUT you have to call it twice each time.
        void showSettingsWindow(int deviceID);

        //Manual control over settings thanks.....
        //These are experimental for now.
        bool setVideoSettingFilter(int deviceID, long Property, long lValue, long Flags = 0, bool useDefaultValue = false);
        bool setVideoSettingFilterPct(int deviceID, long Property, float pctValue, long Flags = 0);
        bool getVideoSettingFilter(int deviceID, long Property, long &min, long &max, long &SteppingDelta, long &currentValue, long &flags, long &defaultValue);

        bool setVideoSettingCamera(int deviceID, long Property, long lValue, long Flags = 0, bool useDefaultValue = false);
        bool setVideoSettingCameraPct(int deviceID, long Property, float pctValue, long Flags = 0);
        bool getVideoSettingCamera(int deviceID, long Property, long &min, long &max, long &SteppingDelta, long &currentValue, long &flags, long &defaultValue);

        //bool setVideoSettingCam(int deviceID, long Property, long lValue, long Flags = NULL, bool useDefaultValue = false);

        //get width, height and number of pixels
        int  getWidth(int deviceID);
        int  getHeight(int deviceID);
        int  getSize(int deviceID);
        int  getFourcc(int deviceID);
        double getFPS(int deviceID);

        //completely stops and frees a device
        void stopDevice(int deviceID);

        //as above but then sets it up with same settings
        bool restartDevice(int deviceID);

        //number of devices available
        int  devicesFound;

        // mapping from OpenCV CV_CAP_PROP to videoinput/dshow properties
        int getVideoPropertyFromCV(int cv_property);
        int getCameraPropertyFromCV(int cv_property);

    private:
        void setPhyCon(int deviceID, int conn);
        void setAttemptCaptureSize(int deviceID, int w, int h,GUID mediaType=MEDIASUBTYPE_RGB24);
        bool setup(int deviceID);
        void processPixels(unsigned char * src, unsigned char * dst, int width, int height, bool bRGB, bool bFlip);
        int  start(int deviceID, videoDevice * VD);
        int  getDeviceCount();
        void getMediaSubtypeAsString(GUID type, char * typeAsString);
        GUID *getMediaSubtypeFromFourcc(int fourcc);
        int    getFourccFromMediaSubtype(GUID type);

        void getVideoPropertyAsString(int prop, char * propertyAsString);
        void getCameraPropertyAsString(int prop, char * propertyAsString);

        HRESULT getDevice(IBaseFilter **pSrcFilter, int deviceID, WCHAR * wDeviceName, char * nDeviceName);
        static HRESULT ShowFilterPropertyPages(IBaseFilter *pFilter);
        static HRESULT ShowStreamPropertyPages(IAMStreamConfig  *pStream);

        HRESULT SaveGraphFile(IGraphBuilder *pGraph, WCHAR *wszPath);
        HRESULT routeCrossbar(ICaptureGraphBuilder2 **ppBuild, IBaseFilter **pVidInFilter, int conType, GUID captureMode);

        //don't touch
        static bool comInit();
        static bool comUnInit();

        int  connection;
        int  callbackSetCount;
        bool bCallback;

        GUID CAPTURE_MODE;

        //Extra video subtypes
        GUID MEDIASUBTYPE_Y800;
        GUID MEDIASUBTYPE_Y8;
        GUID MEDIASUBTYPE_GREY;

        videoDevice * VDList[VI_MAX_CAMERAS];
        GUID mediaSubtypes[VI_NUM_TYPES];
        long formatTypes[VI_NUM_FORMATS];

        static void __cdecl basicThread(void * objPtr);

        static char deviceNames[VI_MAX_CAMERAS][255];

};

///////////////////////////  HANDY FUNCTIONS  /////////////////////////////

static void MyFreeMediaType(AM_MEDIA_TYPE& mt){
    if (mt.cbFormat != 0)
    {
        CoTaskMemFree((PVOID)mt.pbFormat);
        mt.cbFormat = 0;
        mt.pbFormat = NULL;
    }
    if (mt.pUnk != NULL)
    {
        // Unecessary because pUnk should not be used, but safest.
        mt.pUnk->Release();
        mt.pUnk = NULL;
    }
}

static void MyDeleteMediaType(AM_MEDIA_TYPE *pmt)
{
    if (pmt != NULL)
    {
        MyFreeMediaType(*pmt);
        CoTaskMemFree(pmt);
    }
}

//////////////////////////////  CALLBACK  ////////////////////////////////

//Callback class
class SampleGrabberCallback : public ISampleGrabberCB{
public:

    //------------------------------------------------
    SampleGrabberCallback(){
        InitializeCriticalSection(&critSection);
        freezeCheck = 0;


        bufferSetup         = false;
        newFrame            = false;
        latestBufferLength  = 0;

        hEvent = CreateEvent(NULL, true, false, NULL);
    }


    //------------------------------------------------
    virtual ~SampleGrabberCallback(){
        ptrBuffer = NULL;
        DeleteCriticalSection(&critSection);
        CloseHandle(hEvent);
        if(bufferSetup){
            delete[] pixels;
        }
    }


    //------------------------------------------------
    bool setupBuffer(int numBytesIn){
        if(bufferSetup){
            return false;
        }else{
            numBytes            = numBytesIn;
            pixels              = new unsigned char[numBytes];
            bufferSetup         = true;
            newFrame            = false;
            latestBufferLength  = 0;
        }
        return true;
    }


    //------------------------------------------------
    STDMETHODIMP_(ULONG) AddRef() { return 1; }
    STDMETHODIMP_(ULONG) Release() { return 2; }


    //------------------------------------------------
    STDMETHODIMP QueryInterface(REFIID, void **ppvObject){
        *ppvObject = static_cast<ISampleGrabberCB*>(this);
        return S_OK;
    }


    //This method is meant to have less overhead
    //------------------------------------------------
    STDMETHODIMP SampleCB(double , IMediaSample *pSample){
        if(WaitForSingleObject(hEvent, 0) == WAIT_OBJECT_0) return S_OK;

        HRESULT hr = pSample->GetPointer(&ptrBuffer);

        if(hr == S_OK){
            latestBufferLength = pSample->GetActualDataLength();
              if(latestBufferLength == numBytes){
                EnterCriticalSection(&critSection);
                      memcpy(pixels, ptrBuffer, latestBufferLength);
                    newFrame    = true;
                    freezeCheck = 1;
                LeaveCriticalSection(&critSection);
                SetEvent(hEvent);
            }else{
                printf("ERROR: SampleCB() - buffer sizes do not match\n");
            }
        }

        return S_OK;
    }


    //This method is meant to have more overhead
    STDMETHODIMP BufferCB(double, BYTE *, long){
        return E_NOTIMPL;
    }

    int freezeCheck;

    int latestBufferLength;
    int numBytes;
    bool newFrame;
    bool bufferSetup;
    unsigned char * pixels;
    unsigned char * ptrBuffer;
    CRITICAL_SECTION critSection;
    HANDLE hEvent;
};


//////////////////////////////  VIDEO DEVICE  ////////////////////////////////

// ----------------------------------------------------------------------
//    Should this class also be the callback?
//
// ----------------------------------------------------------------------

videoDevice::videoDevice(){

     pCaptureGraph      = NULL;    // Capture graph builder object
     pGraph             = NULL;    // Graph builder object
     pControl           = NULL;    // Media control object
     pVideoInputFilter  = NULL; // Video Capture filter
     pGrabber           = NULL; // Grabs frame
     pDestFilter        = NULL; // Null Renderer Filter
     pGrabberF          = NULL; // Grabber Filter
     pMediaEvent        = NULL;
     streamConf         = NULL;
     pAmMediaType       = NULL;

     //This is our callback class that processes the frame.
     sgCallback           = new SampleGrabberCallback();
     sgCallback->newFrame = false;

     //Default values for capture type
     videoType          = MEDIASUBTYPE_RGB24;
     connection         = PhysConn_Video_Composite;
     storeConn          = 0;

     videoSize          = 0;
     width              = 0;
     height             = 0;

     tryWidth           = 640;
     tryHeight          = 480;
     tryVideoType = MEDIASUBTYPE_RGB24;
     nFramesForReconnect= 10000;
     nFramesRunning     = 0;
     myID               = -1;

     tryDiffSize        = true;
     useCrossbar        = false;
     readyToCapture     = false;
     sizeSet            = false;
     setupStarted       = false;
     specificFormat     = false;
     autoReconnect      = false;
     requestedFrameTime = -1;

     memset(wDeviceName, 0, sizeof(WCHAR) * 255);
     memset(nDeviceName, 0, sizeof(char) * 255);

}


// ----------------------------------------------------------------------
//    The only place we are doing new
//
// ----------------------------------------------------------------------

void videoDevice::setSize(int w, int h){
    if(sizeSet){
        if(verbose)printf("SETUP: Error device size should not be set more than once \n");
    }
    else
    {
        width               = w;
        height              = h;
        videoSize           = w*h*3;
        sizeSet             = true;
        pixels              = new unsigned char[videoSize];
        pBuffer             = new char[videoSize];

        memset(pixels, 0 , videoSize);
        sgCallback->setupBuffer(videoSize);

    }
}


// ----------------------------------------------------------------------
/