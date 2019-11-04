# coding: utf-8

from objc_util import *
import time

AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCapturePhotoOutput = ObjCClass('AVCapturePhotoOutput')

@on_main_thread
def manualCapture(device, output, focusDistance, fileName, fl):
    def captureOutput_didFinishProcessingPhotoSampleBuffer_previewPhotoSampleBuffer_resolvedSettings_bracketSettings_error_(_self, _cmd, _output, _photoBuffer, _previewBuffer, _resolveSettings, bracketSettings, _error):
        photoBuffer = ObjCInstance(_photoBuffer)
        jpegPhotoData = ObjCClass(
            'AVCapturePhotoOutput'
        ).JPEGPhotoDataRepresentationForJPEGSampleBuffer_previewPhotoSampleBuffer_(
            photoBuffer, _previewBuffer)
        jpegPhotoData.writeToFile_atomically_(fileName, True)

    # delegate
    CameraManualPhotoCaptureDelegate = create_objc_class('CameraManualPhotoCaptureDelegate',methods=[captureOutput_didFinishProcessingPhotoSampleBuffer_previewPhotoSampleBuffer_resolvedSettings_bracketSettings_error_],protocols=['AVCapturePhotoCaptureDelegate'])

    device.lockForConfiguration_(None)
    device.setFocusModeLockedWithLensPosition_completionHandler_(
        focusDistance, None)
    device.unlockForConfiguration()

    time.sleep(0.1)
    delegate = CameraManualPhotoCaptureDelegate.new()
    settings = ObjCClass('AVCapturePhotoSettings').photoSettings()
    settings.AVCaptureFocusMode = 0
    if fl:
        settings.flashMode = 1
    else:
        settings.flashMode = 0
    output.capturePhotoWithSettings_delegate_(settings, delegate)
    time.sleep(0.1)
    delegate.release()


@on_main_thread
def camera(flash):
    session = AVCaptureSession.alloc().init()
    device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
    _input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
    if _input:
        session.addInput_(_input)
    else:
        return

    session.startRunning()
    output = AVCapturePhotoOutput.alloc().init()
    session.addOutput_(output)
    time.sleep(0.2)
    manualCapture(device, output, 0.7, 'sample.jpg', flash)
    time.sleep(2) if flash else time.sleep(0.1)
    session.stopRunning()
    session.release()
    output.release()


@on_main_thread
def main():
    session = AVCaptureSession.alloc().init()
    device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
    _input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
    if _input:
        session.addInput_(_input)
    else:
        return

    session.startRunning()
    output = AVCapturePhotoOutput.alloc().init()
    session.addOutput_(output)
    time.sleep(1)
    manualCapture(device, output, 0.0, 'sample.jpg', True)
    time.sleep(2)
    session.stopRunning()
    session.release()
    output.release()


if __name__ == '__main__':
    main()

