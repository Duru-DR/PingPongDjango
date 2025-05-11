FROM nginx:1.27.0-alpine

COPY crtf/certificate.crt /etc/ssl/fttran_tech/
COPY crtf/private.key /etc/ssl/fttran_tech/
COPY crtf/ca_bundle.crt /etc/ssl/fttran_tech/

COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["nginx"]

CMD ["-g", "daemon off;"]