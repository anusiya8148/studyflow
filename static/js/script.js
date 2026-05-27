document.addEventListener('DOMContentLoaded', function () {
  // Mobile Sidebar Drawer Controller Toggle
  const mobileMenuTrigger = document.getElementById('mobileMenuTrigger');
  const applicationSidebar = document.getElementById('applicationSidebar');

  if (mobileMenuTrigger && applicationSidebar) {
    mobileMenuTrigger.addEventListener('click', function () {
      applicationSidebar.classList.toggle('visible');
    });
  }

  // Auto Dismiss Notification Banners
  const dynamicToasts = document.querySelectorAll('.toast-alert');
  dynamicToasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.transition = 'opacity 0.5s ease-out';
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 500);
    }, 4500);
  });
});

// Dynamic Base Layer Core Modal Trigger Bindings
definerModalContext = {
  open: function (modalElementId) {
    const modal = document.getElementById(modalElementId);
    if (modal) modal.style.display = 'flex';
  },
  close: function (modalElementId) {
    const modal = document.getElementById(modalElementId);
    if (modal) modal.style.display = 'none';
  },
};

// Async Random Quote Rotation Engine Engine
async function rotateInspirationalQuote() {
  const frame = document.getElementById('motivationalDisplayQuote');
  if (!frame) return;
  try {
    const response = await fetch('/api/quote');
    const data = await response.json();
    frame.style.opacity = '0';
    setTimeout(() => {
      frame.innerText = `"${data.quote}"`;
      frame.style.opacity = '1';
    }, 200);
  } catch (e) {
    console.error('Quote fetching sync broken: ', e);
  }
}

// Media Streaming Pipeline Block For Voice Captures
let audioMediaRecorder;
let rawAudioBlobs = [];

async function toggleVoiceRecordingState() {
  const actionBtn = document.getElementById('audioRecordBtn');
  const labelState = document.getElementById('recordingStatusText');

  if (!actionBtn) return;

  if (!audioMediaRecorder || audioMediaRecorder.state === 'inactive') {
    rawAudioBlobs = [];
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });
      audioMediaRecorder = new MediaRecorder(mediaStream, {
        mimeType: 'audio/webm',
      });

      audioMediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) rawAudioBlobs.push(event.data);
      };

      audioMediaRecorder.onstop = async () => {
        const finalAudioBlob = new Blob(rawAudioBlobs, { type: 'audio/webm' });
        const recordingTitle =
          prompt('Provide an identifier name title for this clip:') ||
          'New Audio Fragment';

        const serverPayload = new FormData();
        serverPayload.append('audio_data', finalAudioBlob, 'payload.webm');
        serverPayload.append('title', recordingTitle);

        labelState.innerText = 'Processing streaming media upload...';

        try {
          const response = await fetch('/voice', {
            method: 'POST',
            body: serverPayload,
          });
          if (response.ok) {
            window.location.reload();
          } else {
            alert('Server declined modern data payload transfer block.');
            labelState.innerText = 'Error encountered.';
          }
        } catch (err) {
          console.error(err);
          labelState.innerText = 'Network connection pipeline failure.';
        }
      };

      audioMediaRecorder.start(250);
      actionBtn.classList.add('recording');
      actionBtn.innerHTML = '<i class="fas fa-stop"></i>';
      labelState.innerText =
        'Streaming live audio from hardware capture line...';
    } catch (mediaError) {
      alert('Application lack audio hardware mic access permissions.');
      console.error(mediaError);
    }
  } else {
    audioMediaRecorder.stop();
    audioMediaRecorder.stream.getTracks().forEach((track) => track.stop());
    actionBtn.classList.remove('recording');
    actionBtn.innerHTML = '<i class="fas fa-microphone"></i>';
  }
}
