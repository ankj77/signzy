from rest_framework.renderers import JSONRenderer


class TreeboJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'status': 'success', 'data': data}
        return super(TreeboJSONRenderer, self).render(data, accepted_media_type, renderer_context)
