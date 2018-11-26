Simple classes to do basic things with AMX Video-over-IP
encoders and decoders.

YMMV depending on software versions, as device status keys
are liable to change with software releases.

For example, to switch decoder `a` to use the stream from
encoder `b`:

```python
import amx_control

ENCODER_IP = "10.0.0.1"
DECODER_IP = "10.0.0.2"

a = amx_control.AMXDecoder(DECODER_IP)
b = amx_control.AMXEncoder(ENCODER_IP)

a.set_stream(b.stream_id)
```
